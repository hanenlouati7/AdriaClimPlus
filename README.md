# 🌊 Sub-Regional Climate Downscaling over the Adriatic Sea Area

### Part of the [AdriaClimPlus Project](https://www.cmcc.it/projects/adriaclimplus)

---

## 📖 Overview
The Adriatic Sea  a semi-enclosed basin of the Mediterranean Sea — is characterized by complex oceanographic dynamics and strong air–sea interactions. Its shallow northern sector, high riverine input, and marked seasonal variability make it particularly vulnerable to climate change.

This repository documents the **sub-regional climate downscaling** activities carried out over the Adriatic Sea within the *AdriaClimPlus* project. The objective is to generate **high-resolution climate information** that enhances understanding of future oceanographic and atmospheric changes in this sensitive basin.

---

## 🎯 Objectives
- Develop a **sub-regional climate downscaling framework** tailored to the Adriatic region  
- Assess variability and projected changes under the **SSP5-8.5** high-emission scenario  
- Analyze:
  - 10 m wind speed  
  - 2 m air temperature  
  - Precipitation  
  - SST, SSS, SSH, total sea level, and circulation patterns  
- Evaluate the **impacts of river discharges** during the projection period
- Simulations cover:
  - **Historical:** 1985–2014  
  - **Projection:** 2021–2050 (SSP5–8.5)
- Compare and highlight **expected climate trends and variability** within the Adriatic system  

---
## 🧩 Models
Downscaling integrates **dynamical models**:

| Model | Version | Domain | Resolution |
|--------|----------|---------|-------------|
| NEMO | 4.2 | Ocean circulation | ~2 km |
| WRF | 4.4.1 | Atmosphere | ~6 km |
| WRF-Hydro | 3.7 | Hydrology | ~600 m |
> The scripts and workflows included in this repository have also been used in the **AdriaClim** project, the initiative that preceded *AdriaClimPlus*, ensuring **methodological continuity, reproducibility, and consistency** across both projects.


---

## 👥 Developers / Maintainers

- 👍 (MD) **Giorgia Verri** [✉️](mailto:giorgia.verri@cmcc.it) 
- 👍 (MD) **Alessandro De Lorenzis** [✉️](mailto:alessandro.delorenzis@cmcc.it) 
- 👍 (MD) **Renata Eidt** [✉️](mailto:renata.eidt@cmcc.it) 
- 👍 (MD) **Veeramanikandan Ramadoss** [✉️](mailto:veeramanikandan.ramadoss@cmcc.it) 
- 👍 (MD) **Vladimir Santos da Costa** [✉️](mailto:vladimir.santosdacosta@cmcc.it)
- 👍 (M) **Fabio Viola** [✉️](mailto:fabio.viola@cmcc.it)  
- 👍 (M) **Hanen Louati** [✉️](mailto:hanen.louati@cmcc.it)
  
## 📁 Repository Structure

AdriaClimPlusRepo/
```
│
├── ocean/         # Ocean pre/post-processing scripts (NEMO)
├── atmosphere/    
├── hydrology/     
└── README.md      # Project documentation (this file)
└── .gitignore     # extensions that are removed from repository 
```

---


## 📜 License
This repository is intended for collaborative research within the AdriaClimPlus framework.  
Re-use and redistribution are allowed under CMCC collaboration agreements.

