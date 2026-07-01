# Weather-map
 Interactive 3D Globe with live weather and country information.
# 🌍 3D Weather Globe

An interactive 3D globe application built with **Django**, **Three.js**, and **Three-Globe**. Users can explore countries around the world and view real-time weather conditions along with geographic information.

## ✨ Features

* Interactive 3D Earth visualization
* Country selection with mouse interaction
* Real-time weather information
* Country details:

  * Official name
  * Capital city
  * Population
  * Area
  * Currency
  * Language
  * Coordinates
* Smooth camera animations
* Country labels
* Auto-rotating globe

## 🛠️ Technologies

* Python
* Django
* PostgreSQL
* JavaScript
* Three.js
* Three-Globe
* HTML
* CSS
* GeoJSON
* OpenWeather API
* REST API

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/3d-weather-globe.git
cd 3d-weather-globe
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DEBUG=True

DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

WEATHER_API_KEY=your_api_key
```

Apply migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```



## 📄 License

This project is licensed under the MIT License.
