window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            const {
                color,
                selected
            } = feature.properties;
            return {
                fillColor: color || '#CCCCCC',
                fillOpacity: selected ? 0.9 : 0.65,
                color: selected ? '#FF6B00' : '#2E86AB',
                weight: selected ? 4 : 2,
                opacity: 1
            };
        }
    }
});