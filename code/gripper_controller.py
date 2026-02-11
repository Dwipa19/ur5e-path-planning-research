from controller import Robot, Supervisor
import math
import random

# --- KONFIGURASI ---
Q_START = [0.0, -1.57, 0.0, -1.57, 0.0, 0.0]
# Obstacle sementara
OBSTACLE = {'x': 0.45, 'y': 0.05, 'radius': 0.25}

class AdvancedIK:
    @staticmethod
    def solve_horizontal(target_x, target_y, target_z_floor):
        # --- DIMENSI UR5e (Meter) ---
        d1 = 0.1625
        a2 = 0.425
        a3 = 0.392
        d4 = 0.1091
        d6 = 0.0823
        
        shoulder_offset = 0.13
        
        # --- PERBAIKAN UTAMA: MUNDURKAN WRIST ---
        # Sebelumnya 0.12 (Terlalu Maju -> Nabrak)
        # Sekarang 0.17 (Mundur 5cm -> Aman)
        gripper_len = 0.17 
        
        # Target Z (Tengah Kaleng)
        z_target = target_z_floor + 0.06 
        
        # Hitung Jarak & Sudut ke Botol
        dist_to_bottle = math.sqrt(target_x**2 + target_y**2)
        angle_to_bottle = math.atan2(target_y, target_x)
        
        # Posisi Wrist (Mundur dari botol sejauh gripper_len)
        r_wrist = dist_to_bottle - gripper_len
        w_x = r_wrist * math.cos(angle_to_bottle)
        w_y = r_wrist * math.sin(angle_to_bottle)
        w_z = z_target
        
        # --- 1. BASE PAN (Theta 1) ---
        try:
            correction_angle = math.asin(shoulder_offset / r_wrist)
        except ValueError:
            return None
        theta1 = angle_to_bottle - correction_angle

        # --- 2. JANGKAUAN LENGAN ---
        r_reach = math.sqrt(r_wrist**2 - shoulder_offset**2)
        h_reach = w_z - d1
        c_len = math.sqrt(r_reach**2 + h_reach**2)
        
        if c_len > (a2 + a3):
            print("IK LIMIT: Kurang panjang!")
            return None

        # --- 3. SIKU & BAHU (Theta 2 & 3) ---
        cos_beta = (a2**2 + c_len**2 - a3**2) / (2 * a2 * c_len)
        cos_gamma = (a2**2 + a3**2 - c_len**2) / (2 * a2 * a3)
        
        beta = math.acos(max(-1.0, min(1.0, cos_beta)))
        gamma = math.acos(max(-1.0, min(1.0, cos_gamma)))
        alpha = math.atan2(h_reach, r_reach)
        
        theta2 = -(alpha + beta)
        theta3 = math.pi - gamma
        
        # --- 4. ORIENTASI HORIZONTAL ---
        theta4 = - (theta2 + theta3)
        theta5 = -1.57 
        theta6 = 1.57 # Putar gripper miring (Side Grasp)

        return [theta1, theta2, theta3, theta4, theta5, theta6]

class Node:
    def __init__(self, q):
        self.q = q
        self.parent = None

class RRTPlanner:
    def __init__(self):
        self.robot = Supervisor()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.robot_node = self.robot.getSelf()
        self.target_node = self.robot.getFromDef("TARGET_BOTOL")
        
        self.joint_names = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", 
                            "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
        self.motors = []
        for name in self.joint_names:
            m = self.robot.getDevice(name)
            if m:
                m.setVelocity(1.0)
                self.motors.append(m)
        
        self.gripper_motors = []
        g_names = ["ROBOTIQ 2F-85 Gripper::left finger joint", "ROBOTIQ 2F-85 Gripper::right finger joint"]
        for g_name in g_names:
            g = self.robot.getDevice(g_name)
            if g:
                g.setVelocity(1.0)
                g.setAvailableTorque(100.0)
                self.gripper_motors.append(g)

    def dist(self, q1, q2):
        return math.sqrt(sum((q1[i] - q2[i])**2 for i in range(len(q1))))

    def is_collision(self, q):
        return False 

    def plan(self, q_start, q_goal):
        print("Mencari jalur RRT...")
        nodes = [Node(q_start)]
        for i in range(3000):
            if random.random() < 0.2: q_rand = q_goal
            else: q_rand = [random.uniform(-3.14, 3.14) for _ in range(6)]
            
            nearest = min(nodes, key=lambda n: self.dist(n.q, q_rand))
            step = 0.15
            direc = [(q_rand[j] - nearest.q[j]) for j in range(6)]
            length = math.sqrt(sum(x**2 for x in direc))
            if length == 0: continue
            q_new = [(nearest.q[j] + (direc[j]/length) * step) for j in range(6)]
            
            new_node = Node(q_new)
            new_node.parent = nearest
            nodes.append(new_node)
            if self.dist(q_new, q_goal) < 0.15:
                print(f"Jalur ketemu! (Iterasi {i})")
                path = []
                curr = new_node
                while curr:
                    path.append(curr.q)
                    curr = curr.parent
                path.append(q_goal)
                return path[::-1]
        print("RRT Timeout. Pakai jalur lurus.")
        return [q_start, q_goal]

    def run(self):
        print("--- SYSTEM START (OFFSET CORRECTED) ---")
        if self.target_node is None:
            print("ERROR: DEF 'TARGET_BOTOL' tidak ditemukan!")
            return

        target_pos = self.target_node.getPosition()
        robot_pos  = self.robot_node.getPosition()
        
        rel_x = target_pos[0] - robot_pos[0]
        rel_y = target_pos[1] - robot_pos[1]
        rel_z = target_pos[2] - robot_pos[2] 

        print(f"Target Relatif: X={rel_x:.2f}, Y={rel_y:.2f}")

        # HITUNG IK
        q_ik = AdvancedIK.solve_horizontal(rel_x, rel_y, rel_z)
        
        if q_ik is None:
            print("ERROR: Tangan tidak sampai!")
            return
        
        # Standby
        for i in range(6): self.motors[i].setPosition(Q_START[i])
        for g in self.gripper_motors: g.setPosition(0.0)
        for _ in range(30): self.robot.step(self.timestep)
        
        # Gerak
        path = self.plan(Q_START, q_ik)
        
        idx = 0
        wait = 0
        print("Bergerak...")
        while self.robot.step(self.timestep) != -1:
            if idx < len(path):
                target = path[idx]
                for i in range(6): self.motors[i].setPosition(target[i])
                wait += 1
                if wait > 2:
                    idx += 1
                    wait = 0
            else:
                wait += 1
                if wait > 20: 
                    # GRIP (Side Hug)
                    for g in self.gripper_motors: g.setPosition(0.79)

if __name__ == "__main__":
    rrt = RRTPlanner()
    rrt.run()