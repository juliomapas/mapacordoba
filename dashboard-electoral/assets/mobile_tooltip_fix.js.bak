/**
 * Script para ajustar tooltips de Folium en dispositivos móviles
 * - Fuerza estilos responsive
 * - Posiciona tooltips en el centro del mapa en móvil
 */

// Función para detectar si es móvil
function isMobileDevice() {
    return window.innerWidth <= 768;
}

// Función para centrar tooltip en el mapa
function centerTooltipInMap(tooltip, mapContainer) {
    if (!isMobileDevice()) return;

    // Obtener dimensiones del contenedor del mapa
    const mapRect = mapContainer.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();

    // Calcular posición central
    const centerX = (mapRect.width / 2) - (tooltipRect.width / 2);
    const centerY = (mapRect.height / 2) - (tooltipRect.height / 2);

    // Aplicar posición fija en el centro
    tooltip.style.position = 'fixed';
    tooltip.style.left = (mapRect.left + centerX) + 'px';
    tooltip.style.top = (mapRect.top + centerY) + 'px';
    tooltip.style.transform = 'none'; // Remover transformaciones de Leaflet
    tooltip.style.zIndex = '9999';
}

// Función para aplicar estilos y posicionar tooltips
function applyMobileTooltipStyles() {
    const iframe = document.getElementById('electoral-map');
    if (!iframe) return;

    try {
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        const mapContainer = iframeDoc.querySelector('.leaflet-container');
        if (!mapContainer) return;

        // Observar cambios en el DOM del iframe para capturar tooltips dinámicos
        const observer = new MutationObserver(function(mutations) {
            const tooltips = iframeDoc.querySelectorAll('.leaflet-tooltip');

            tooltips.forEach(function(tooltip) {
                // Forzar estilos para móvil
                const isMobile = window.innerWidth <= 480;
                const isTablet = window.innerWidth <= 768 && window.innerWidth > 480;

                if (isMobile) {
                    tooltip.style.fontSize = '7px';
                    tooltip.style.padding = '2px 4px';
                    tooltip.style.maxWidth = '90px';
                    tooltip.style.lineHeight = '1.0';
                    tooltip.style.fontWeight = 'normal';
                } else if (isTablet) {
                    tooltip.style.fontSize = '8px';
                    tooltip.style.padding = '3px 5px';
                    tooltip.style.maxWidth = '110px';
                    tooltip.style.lineHeight = '1.1';
                    tooltip.style.fontWeight = 'normal';
                }

                // Aplicar a elementos hijos también
                const children = tooltip.querySelectorAll('*');
                children.forEach(function(child) {
                    child.style.fontWeight = 'normal';
                    if (isMobile) {
                        child.style.fontSize = '7px';
                    } else if (isTablet) {
                        child.style.fontSize = '8px';
                    }
                });

                // CENTRAR tooltip en dispositivos móviles
                if (isMobileDevice() && tooltip.style.opacity !== '0') {
                    setTimeout(function() {
                        centerTooltipInMap(tooltip, iframe);
                    }, 10);
                }
            });
        });

        // Configurar el observer
        observer.observe(iframeDoc.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['style', 'class']
        });

        // Aplicar estilos iniciales
        setTimeout(function() {
            const tooltips = iframeDoc.querySelectorAll('.leaflet-tooltip');
            tooltips.forEach(function(tooltip) {
                const isMobile = window.innerWidth <= 480;
                const isTablet = window.innerWidth <= 768 && window.innerWidth > 480;

                if (isMobile) {
                    tooltip.style.fontSize = '7px';
                    tooltip.style.padding = '2px 4px';
                    tooltip.style.maxWidth = '90px';
                    tooltip.style.fontWeight = 'normal';
                } else if (isTablet) {
                    tooltip.style.fontSize = '8px';
                    tooltip.style.padding = '3px 5px';
                    tooltip.style.maxWidth = '110px';
                    tooltip.style.fontWeight = 'normal';
                }

                if (isMobileDevice()) {
                    centerTooltipInMap(tooltip, iframe);
                }
            });
        }, 1000);

        // Interceptar eventos de mouseover/touchstart en el mapa
        if (isMobileDevice()) {
            mapContainer.addEventListener('touchstart', function() {
                setTimeout(function() {
                    const tooltips = iframeDoc.querySelectorAll('.leaflet-tooltip');
                    tooltips.forEach(function(tooltip) {
                        if (tooltip.style.opacity !== '0') {
                            centerTooltipInMap(tooltip, iframe);
                        }
                    });
                }, 50);
            });

            mapContainer.addEventListener('touchmove', function(e) {
                // Prevenir scroll mientras se toca el mapa
                const tooltips = iframeDoc.querySelectorAll('.leaflet-tooltip');
                tooltips.forEach(function(tooltip) {
                    if (tooltip.style.opacity !== '0') {
                        centerTooltipInMap(tooltip, iframe);
                    }
                });
            });
        }

    } catch (e) {
        console.log('No se puede acceder al contenido del iframe:', e);
    }
}

// Ejecutar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(applyMobileTooltipStyles, 500);
    });
} else {
    setTimeout(applyMobileTooltipStyles, 500);
}

// Reaplica en cambios de tamaño de ventana
window.addEventListener('resize', function() {
    setTimeout(applyMobileTooltipStyles, 300);
});

// Reaplica en cambios de orientación
window.addEventListener('orientationchange', function() {
    setTimeout(applyMobileTooltipStyles, 500);
});

// Reaplica cuando se actualiza el mapa (callbacks de Dash)
if (window.dash_clientside) {
    window.dash_clientside = window.dash_clientside || {};
    window.dash_clientside.clientside = {
        refresh_tooltips: function() {
            setTimeout(applyMobileTooltipStyles, 500);
            return window.dash_clientside.no_update;
        }
    };
}
