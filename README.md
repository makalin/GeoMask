# GeoMask 🗺️🕵️‍♂️

**Protect your privacy from AI-powered GeoGuessr tools.**

![geomask](logo.png)

GeoMask lets you upload photos intended for social media, then automatically replaces the identifiable background view (e.g., your window’s scenery) with a decoy — a different city, a Swiss mountain village, or a custom scene of your choice.

---

## 🚀 Features

* 🌐 Replace window views with AI-generated decoy locations
* 🏙️ Choose from presets: cityscapes, nature, mountains, seaside, etc.
* 🔒 Prevent AI-based geolocation or doxxing
* 🖼️ High-resolution output ready for social media
* 🧠 Powered by local or cloud-based AI image generation

---

## 💻 Tech Stack

* Python (FastAPI or Flask)
* OpenAI API / Stable Diffusion (for image generation)
* OpenCV / PIL (image processing)
* React (frontend, optional)
* Docker (optional for deployment)

---

## 📦 Installation

```bash
git clone https://github.com/makalin/GeoMask.git  
cd GeoMask  
pip install -r requirements.txt  
python app.py  
```

Or use the Docker image:

```bash
docker build -t geomask .  
docker run -p 5000:5000 geomask  
```

---

## ⚡ Usage

1️⃣ Upload a photo with a window or background you want to mask.
2️⃣ Choose a decoy scene or let GeoMask randomize it.
3️⃣ Download the protected photo — ready for posting!

---

## 🌟 Example

![geomask](example.png)

---

## 🛡️ Why GeoMask?

Modern AI tools can analyze window views, skyline patterns, and environmental cues in photos to guess your location — sometimes within meters. GeoMask ensures your privacy by swapping these views with decoy scenes.

---

## 📄 License

MIT License

---

## 🤝 Contributing

PRs welcome! Please open an issue first to discuss proposed changes.
