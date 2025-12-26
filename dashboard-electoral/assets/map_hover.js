// Efecto hover para el mapa electoral
// Este script agrega interactividad al pasar el mouse sobre las seccionales del mapa MapLibre

console.log('Map hover script loading...');

// Función para aplicar efectos hover al mapa MapLibre
function applyMapHoverEffects() {
    console.log('Applying map hover effects');

    const mapElement = document.getElementById('electoral-map');
    if (!mapElement) {
        console.log('Map element not found, retrying...');
        return false;
    }

    // Buscar el canvas de MapLibre dentro del elemento del mapa
    const canvas = mapElement.querySelector('.maplibregl-canvas, .mapboxgl-canvas, canvas');
    if (canvas) {
        console.log('Found map canvas, hover will be handled by Plotly/MapLibre');
        canvas.style.cursor = 'pointer';
        return true;
    }

    // Si no hay canvas, buscar elementos SVG (fallback para otros tipos de mapas)
    const svgElements = mapElement.querySelectorAll('svg path, .geolayer path, .choroplethmapbox path');
    if (svgElements.length > 0) {
        console.log('Found ' + svgElements.length + ' SVG paths, applying hover effects');

        svgElements.forEach(function(path) {
            const originalStroke = window.getComputedStyle(path).stroke || '#2E86AB';
            const originalStrokeWidth = window.getComputedStyle(path).strokeWidth || '1.8';
            const originalFillOpacity = window.getComputedStyle(path).fillOpacity || '0.65';

            path.addEventListener('mouseenter', function() {
                this.style.stroke = '#1a5276';
                this.style.strokeWidth = '3px';
                this.style.fillOpacity = '0.85';
                this.style.transition = 'all 0.2s ease';
                this.style.cursor = 'pointer';
            });

            path.addEventListener('mouseleave', function() {
                this.style.stroke = originalStroke;
                this.style.strokeWidth = originalStrokeWidth;
                this.style.fillOpacity = originalFillOpacity;
            });
        });
        return true;
    }

    return false;
}

// Intentar aplicar efectos cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(applyMapHoverEffects, 1500);
    });
} else {
    setTimeout(applyMapHoverEffects, 1500);
}

// Observador de mutaciones para detectar cuando se renderice el mapa
const observer = new MutationObserver(function(mutations) {
    const mapElement = document.getElementById('electoral-map');
    if (mapElement) {
        const hasCanvas = mapElement.querySelector('.maplibregl-canvas, .mapboxgl-canvas, canvas');
        const hasSVG = mapElement.querySelectorAll('svg path, .geolayer path').length > 0;

        if (hasCanvas || hasSVG) {
            console.log('Map detected, applying effects');
            if (applyMapHoverEffects()) {
                observer.disconnect();
            }
        }
    }
});

// Iniciar observación del body
if (document.body) {
    observer.observe(document.body, { childList: true, subtree: true });
}

// Evento de Plotly para reaplicar efectos después de redibujado
document.addEventListener('plotly_afterplot', function(event) {
    if (event.target && event.target.id === 'electoral-map') {
        console.log('Map replotted, reapplying hover effects');
        setTimeout(function() {
            applyMapHoverEffects();
        }, 500);
    }
});

console.log('Map hover script loaded successfully');
