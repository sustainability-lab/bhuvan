// geostats.js

// Function to calculate total area in square meters for polygons and multipolygons
function calculateTotalArea(data) {
    let totalAreaSqMeters = 0;

    // Loop through each feature and accumulate area if it’s a polygon or multipolygon
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
    // Filter to include only polygons and multipolygons
    const polygonsOnly = {
        type: "FeatureCollection",
        features: data.features.filter(f => f.geometry.type === "Polygon" || f.geometry.type === "MultiPolygon")
    };

    return turf.centroid(polygonsOnly);
}