# UR5e Path Planning dengan RRT di Webots

Path planning implementation untuk robot UR5e menggunakan algoritma RRT (Rapidly-exploring Random Trees) di simulator Webots.

## 📖 Tentang Penelitian

**Topik:** Penerapan Path Planning pada Robot UR5e dengan Obstacle Avoidance  
**Platform:** Webots Simulator  
**Robot:** Universal Robots UR5e (6-DOF)  
**Gripper:** ROBOTIQ 2F-85  
**Algoritma:** RRT (Rapidly-exploring Random Trees)

## 🎯 Objectives

1. Implementasi inverse kinematics untuk UR5e
2. Path planning menggunakan RRT algorithm
3. Collision detection dan obstacle avoidance
4. Gripper control untuk object manipulation
5. Integration dan testing di Webots

## 📁 Struktur Project

```
ur5e-research/
├── docs/                           # Dokumentasi
│   ├── integration_spec.md         # Master specification
│   └── draft_skripsi.docx          # Draft skripsi (Bab 1-3)
├── code/                           # Source code
│   └── gripper_controller.py       # Main controller (current)
├── references/                     # Referensi
│   └── 13120022_Salma_...docx     # Template senior
└── notes/                          # Research notes
    └── progress_log.md             # Daily progress
```

## 🔧 Current Status

### ✅ Working:
- Basic RRT path planning
- Analytical IK solver (horizontal orientation)
- Gripper basic control
- Webots integration

### 🚧 In Progress:
- Collision detection implementation
- IK solver improvements
- Gripper force feedback

### ⏳ Planned:
- Path optimization
- Multiple object handling
- Performance benchmarking

## 🚀 Setup Instructions

### Prerequisites:
- Webots R2025a
- Python 3.8+
- UR5e model di Webots
- ROBOTIQ 2F-85 gripper

### Installation:
```bash
# Clone repository
git clone https://github.com/[username]/ur5e-path-planning.git
cd ur5e-path-planning

# Copy controller ke Webots project
cp code/gripper_controller.py [webots_project]/controllers/

# Run di Webots
# Load world file dengan UR5e + target object
```

## 📊 Key Components

### 1. Inverse Kinematics (`AdvancedIK` class)
- Analytical solution untuk horizontal reach
- Handles UR5e DH parameters
- Returns: 6 joint angles [θ1...θ6]

### 2. Path Planning (`RRTPlanner` class)
- Basic RRT implementation
- Goal biasing: 20%
- Max iterations: 3000
- Step size: 0.15 rad

### 3. Gripper Control
- Binary open/close control
- Target position: 0.79 (close)
- Fixed torque: 100.0

## 🎓 Untuk Development

### Development Workflow:
1. Create branch untuk each module
2. Test di Webots sebelum commit
3. Update `integration_spec.md` setelah changes
4. Document di `progress_log.md`

### Coding Standards:
- Python PEP 8 style
- Detailed comments untuk academic documentation
- Clear variable naming (sesuai notation di skripsi)

## 📝 Documentation

Dokumentasi lengkap ada di:
- **Technical:** `docs/integration_spec.md`
- **Progress:** `notes/progress_log.md`
- **Academic:** `docs/draft_skripsi.docx`

## 🐛 Known Issues

1. **CRITICAL:** Collision detection disabled
2. **HIGH:** IK singularity tidak handled
3. **HIGH:** No joint limit validation
4. **MEDIUM:** Path tidak optimal (no smoothing)

Details: Lihat `integration_spec.md` → Prioritas Development

## 📧 Contact

[Nama Anda]  
[Email/GitHub]

## 📄 License

[Your License Choice]

---

**Last Updated:** 11 Februari 2026
