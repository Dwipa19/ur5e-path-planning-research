# Setup Guide: GitHub & Google Drive Integration

**Tujuan:** Menghubungkan project penelitian dengan GitHub (untuk code) dan Google Drive (untuk dokumen) agar terintegrasi dengan Claude Projects.

---

## 🐙 BAGIAN 1: Setup GitHub Repository

### Step 1: Inisialisasi Git Lokal

```bash
cd /path/to/ur5e-research

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: UR5e path planning research setup"
```

### Step 2: Create GitHub Repository

1. Buka https://github.com
2. Klik **"New Repository"**
3. Nama: `ur5e-path-planning-research`
4. Description: `Path planning implementation untuk UR5e robot menggunakan RRT di Webots`
5. **JANGAN** centang "Initialize with README" (sudah ada!)
6. Klik **"Create repository"**

### Step 3: Connect Local to GitHub

```bash
# Add remote
git remote add origin https://github.com/[USERNAME]/ur5e-path-planning-research.git

# Push
git branch -M main
git push -u origin main
```

### Step 4: Verify Upload

- Refresh GitHub page
- Cek file structure:
  ```
  ✓ README.md
  ✓ .gitignore
  ✓ docs/
  ✓ code/
  ✓ references/
  ✓ notes/
  ```

---

## 📁 BAGIAN 2: Setup Google Drive Integration

### Step 1: Organize Google Drive Folder

1. Buka Google Drive
2. Buat folder baru: **"UR5e_Path_Planning_Research"**
3. Struktur internal:

```
UR5e_Path_Planning_Research/
├── 📄 Draft_Skripsi_REVISED.docx
├── 📄 integration_spec.md (copy dari local)
├── 📁 Papers/
│   ├── RRT_Algorithm.pdf
│   ├── UR5e_Kinematics.pdf
│   └── Grasping_Strategies.pdf
├── 📁 Results/
│   └── (screenshots, data, graphs)
└── 📁 References/
    └── 13120022_Salma_Rahmani...docx
```

### Step 2: Upload Files

**Upload ke Drive:**
- Draft skripsi Anda
- File Salma (referensi)
- Integration_spec.md
- Papers yang relevan

**JANGAN upload ke Drive:**
- Code files (pakai GitHub!)
- Large videos
- Temporary files

---

## 🤖 BAGIAN 3: Connect ke Claude Projects

### Step 1: Create Claude Project

1. Buka Claude.ai
2. Sidebar → **"Projects"**
3. Klik **"Create Project"**
4. Nama: `UR5e Path Planning Research`

### Step 2: Add Custom Instructions

Paste ini di **Custom Instructions**:

```
RESEARCH CONTEXT:
- Robot: UR5e (6-DOF manipulator)
- Platform: Webots R2023b
- Goal: Path planning dengan RRT + obstacle avoidance
- Programming: Python 3.x

CURRENT STATUS:
- Bab 1-3 skripsi: DONE
- Bab 4: IN PROGRESS
- Code: gripper_controller.py (needs improvement)

PRIORITY ISSUES:
1. Collision detection (CRITICAL - masih dummy!)
2. IK solver improvements
3. Gripper force feedback

CODE PREFERENCES:
- Modular design (separate files per component)
- Well-commented untuk dokumentasi akademik
- Follow PEP 8 style
- Clear variable names matching skripsi notation

DELIVERABLES:
1. Working collision detection
2. Improved IK solver
3. Enhanced gripper control
4. Benchmark results untuk Bab 4
```

### Step 3: Connect GitHub

1. Di Project → **"Knowledge"** → **"Add"**
2. Pilih **"GitHub"**
3. Authorize Claude untuk akses GitHub
4. Select repository: `ur5e-path-planning-research`
5. **Select specific folders:**
   - ✅ `code/` (semua .py files)
   - ✅ `docs/integration_spec.md`
   - ✅ `README.md`
   - ❌ `references/` (ada di Drive)
   - ❌ `.gitignore`, `.git/`

### Step 4: Connect Google Drive

1. Di Project → **"Knowledge"** → **"Add"**
2. Pilih **"Google Drive"**
3. Authorize Claude
4. Select folder: `UR5e_Path_Planning_Research`
5. **Select specific files:**
   - ✅ Draft_Skripsi_REVISED.docx
   - ✅ integration_spec.md (backup di Drive)
   - ✅ Papers/ (all PDFs)
   - ✅ 13120022_Salma... (referensi)

### Step 5: Verify Integration

**Test di Chat baru:**
```
User: "Lihat gripper_controller.py, apa issue utama di collision detection?"

Claude: [Should access file from GitHub dan bisa jawab!]
```

---

## 🔄 BAGIAN 4: Daily Workflow

### Pagi (Mulai Kerja):

```bash
# 1. Pull latest dari GitHub (jika kolaborasi)
git pull origin main

# 2. Di Claude Project → Klik "Sync now"
#    (Sync GitHub & Drive untuk latest files)

# 3. Mulai chat baru untuk task hari ini
#    Claude sudah punya akses ke semua files!
```

### Coding Session:

```bash
# 1. Edit code lokal (VSCode, PyCharm, dll)

# 2. Test di Webots

# 3. Jika working:
git add code/
git commit -m "Fix: Implement sphere collision detection"
git push origin main

# 4. Update integration_spec.md di Drive
#    (Mark completed tasks, update status)
```

### Sore (Selesai Kerja):

```bash
# 1. Update progress_log.md
git add notes/progress_log.md
git commit -m "Daily log: 11 Feb 2026"
git push

# 2. Di Claude Project → Sync now
#    (Ensure tomorrow's session has latest)

# 3. Brief notes di Google Doc (opsional)
```

---

## 💡 TIPS OPTIMASI TOKEN

### ✅ DO:

1. **Selective Sync di GitHub:**
   - Hanya sync `code/` dan `docs/integration_spec.md`
   - Skip large binary files
   
2. **Organize Drive Strategically:**
   - Papers dalam 1 folder (easy to select/deselect)
   - Working docs terpisah dari archives
   
3. **Update Regularly:**
   - Sync sebelum mulai chat baru
   - Commit code setelah testing
   
4. **Use Integration Spec:**
   - Sebagai "peta" untuk semua chats
   - Update setiap selesai modul

### ❌ DON'T:

1. **Jangan sync everything:**
   - Skip .git/, __pycache__/, venv/
   - Use .gitignore!
   
2. **Jangan upload duplikat:**
   - Code → GitHub only
   - Docs → Drive only
   - Integration spec → Both (backup)
   
3. **Jangan lupa sync:**
   - Out-of-date files = wasted tokens
   - Claude process old versions

---

## 📋 Checklist Setup Lengkap

### GitHub:
- [ ] Repository created
- [ ] Local git initialized
- [ ] First commit pushed
- [ ] .gitignore configured
- [ ] Connected ke Claude Project
- [ ] Test sync working

### Google Drive:
- [ ] Folder structure created
- [ ] Documents uploaded
- [ ] Papers organized
- [ ] Connected ke Claude Project
- [ ] Test access working

### Claude Project:
- [ ] Project created
- [ ] Custom instructions added
- [ ] GitHub connected & synced
- [ ] Google Drive connected & synced
- [ ] Test chat verified access

---

## 🆘 Troubleshooting

**Problem:** Claude tidak bisa akses file dari GitHub  
**Solution:** 
- Check repo is public (atau auth token valid)
- Verify file path di sync settings
- Click "Sync now" manually

**Problem:** Drive files outdated di Claude  
**Solution:**
- Klik "Sync now" sebelum chat
- Check Drive folder permissions
- Re-connect jika perlu

**Problem:** Git push rejected  
**Solution:**
```bash
git pull origin main --rebase
git push origin main
```

---

## ✅ Next Steps Setelah Setup

1. **Test integration:**
   - Buat chat baru
   - Ask Claude tentang code
   - Verify Claude bisa akses

2. **Start development:**
   - Chat 1: Fix collision detection
   - Update code lokal
   - Commit & push
   - Sync Claude Project

3. **Document progress:**
   - Update integration_spec.md
   - Daily entry di progress_log.md
   - Track di GitHub commits

---

**Setup selesai! Siap untuk efficient research workflow! 🚀**
