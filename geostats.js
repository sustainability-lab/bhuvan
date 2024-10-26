// Function to calculate total area in square meters for polygons and multipolygons
function calculateTotalArea(data) {
    let totalAreaSqMeters = 0;

    data.features.forEach(feature => {
        if (feature.geometry.type === "Polygon" || feature.geometry.type === "MultiPolygon") {
            totalAreaSqMeters += turf.area(feature);
        }
    });

    return {
        areaSqMeters: totalAreaSqMeters,
        areaHectares: totalAreaSqMeters / 10000 // Convert to hectares
    };
}

// Function to calculate the centroid of all polygons and multipolygons
function calculateCentroid(data) {
    const polygonsOnly = {
        type: "FeatureCollection",
        features: data.features.filter(f => f.geometry.type === "Polygon" || f.geometry.type === "MultiPolygon")
    };

    return turf.centroid(polygonsOnly);
}

// Function to count different geometry types
function countGeometryTypes(data) {
    const geometryCounts = { Polygon: 0, Point: 0, LineString: 0, MultiPolygon: 0 };

    data.features.forEach(feature => {
        const geomType = feature.geometry.type;
        if (geometryCounts[geomType] !== undefined) {
            geometryCounts[geomType]++;
        }
    });

    return geometryCounts;
}

// Function to retrieve feature names if available
function getFeatureNames(data) {
    const featureNames = [];

    data.features.forEach(feature => {
        if (feature.properties && feature.properties.name) {
            featureNames.push(feature.properties.name);
        }
    });

    return featureNames;
}
