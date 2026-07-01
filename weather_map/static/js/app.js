let hoveredCountry = null;
let countriesData = [];

const globeEl = document.getElementById("globeViz");

const world = Globe()(globeEl)
    .backgroundColor("rgba(0,0,0,0)")
    .showAtmosphere(true)
    .atmosphereColor("#3a9bdc")
    .atmosphereAltitude(0.18)
    .globeImageUrl("//unpkg.com/three-globe/example/img/earth-night.jpg")
    .bumpImageUrl("//unpkg.com/three-globe/example/img/earth-topology.png");

world.controls().autoRotate = true;
world.controls().autoRotateSpeed = 0.4;
world.controls().enableDamping = true;
world.controls().dampingFactor = 0.08;

world.controls().addEventListener("start", () => {
    world.controls().autoRotate = false;
});

showLoading(true);

fetch("/static/data/countries.geo.json")
    .then(res => {
        if (!res.ok) throw new Error("Error retrieving map file");
        return res.json();
    })
    .then(data => {

        countriesData = data.features;

        const labels = countriesData.map(feature => {
            const center = getCenter(feature.geometry.coordinates);
            return {
                name: feature.properties.name || feature.properties.ADMIN,
                lat: center.lat,
                lng: center.lng
            };
        });

        world
            .polygonsData(countriesData)
            .polygonAltitude(d => (d === hoveredCountry ? 0.06 : 0.01))
            .polygonCapColor(d =>
                d === hoveredCountry
                    ? "rgba(0,255,150,0.75)"
                    : "rgba(0,150,255,0.3)"
            )
            .polygonSideColor(() => "rgba(0,100,200,0.15)")
            .polygonStrokeColor(d =>
                d === hoveredCountry ? "#00ff9d" : "rgba(255,255,255,0.4)"
            )
            .polygonsTransitionDuration(300)
            .polygonLabel(d => `
                <div style="
                    background: rgba(10,10,15,0.85);
                    padding: 6px 10px;
                    border-radius: 8px;
                    border: 1px solid #00ff9d;
                    color: #fff;
                    font-size: 13px;
                ">
                    ${d.properties.name || d.properties.ADMIN}
                </div>
            `)
            .onPolygonHover(poly => {
                hoveredCountry = poly;
                globeEl.style.cursor = poly ? "pointer" : "default";
            })
            .labelsData(labels)
            .labelText(d => d.name)
            .labelLat(d => d.lat)
            .labelLng(d => d.lng)
            .labelSize(0.8)
            .labelColor(() => "white")
            .labelDotRadius(0)
            .labelResolution(2)
            .labelAltitude(0.02)
            .onPolygonClick(handleCountryClick);

        showLoading(false);
    })
    .catch(err => {
        console.error(err);
        showLoading(false, "An error occurred while loading the map");
    });

async function handleCountryClick(country) {

    world.controls().autoRotate = false;

    const iso3 =
        country.id ||
        country.properties.iso_a3 ||
        country.properties.ISO_A3 ||
        country.properties.ISO3;

    if (!iso3) {
        console.warn("ISO code not found for this country");
        return;
    }

    showLoading(true);

    try {
        const response = await fetch(`/api/weather/${iso3}/`);

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const weather = await response.json();

        showWeather(weather);

        if (weather.flag) {
            setText("flag", weather.flag);
        }

        const center = getCenter(country.geometry.coordinates);

        world.pointOfView(
            {
                lat: center.lat,
                lng: center.lng,
                altitude: 1.6
            },
            1200
        );

    } catch (err) {
        console.error(err);
        showWeatherError();
    } finally {
        showLoading(false);
    }
}

function showWeather(weather) {

    setText("country", weather.country);
    setText("official_name", weather.official_name);
    setText("capital", weather.capital);
    setText("continent", weather.continent);
    setText("area", weather.area ? `${weather.area} km²` : "-");
    setText("currency", weather.currency);
    setText("language", weather.language);
    setText("latitude", weather.latitude);
    setText("longitude", weather.longitude);

    setText(
        "temperature",
        weather.temperature != null ? `${weather.temperature} °C` : "-"
    );

    setText(
        "feels_like",
        weather.feels_like != null ? `${weather.feels_like} °C` : "-"
    );

    setText(
        "humidity",
        weather.humidity != null ? `${weather.humidity} %` : "-"
    );

    setText(
        "wind_speed",
        weather.wind_speed != null ? `${weather.wind_speed} km/h` : "-"
    );

    setText(
        "pressure",
        weather.pressure != null ? `${weather.pressure} hPa` : "-"
    );

    setText("description", weather.description);

}

function showWeatherError() {
    setText("description", "Failed to retrieve weather information, please try again");
}

function showLoading(state, message) {
    const loader = document.getElementById("loading");
    if (!loader) return;

    loader.style.display = state ? "flex" : "none";

    if (message) {
        loader.innerText = message;
    }
}

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) {
        el.innerText = value ?? "-";
    }
}

function getCenter(coords) {

    let points = [];

    function walk(arr) {
        if (typeof arr[0] === "number") {
            points.push(arr);
        } else {
            arr.forEach(walk);
        }
    }

    walk(coords);

    let lat = 0;
    let lng = 0;

    points.forEach(p => {
        lng += p[0];
        lat += p[1];
    });

    return {
        lat: lat / points.length,
        lng: lng / points.length
    };

}