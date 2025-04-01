modal_js_template = """
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {{
    setTimeout(function() {{
        try {{
            // Node data
            const nodeData = {node_data_json};
            // Legend data
            const legendData = {legend_json};

            // Modal elements
            const modal = document.getElementById('node-modal');
            const modalTitle = document.getElementById('modal-title');
            const modalDate = document.getElementById('modal-date');
            const modalCountry = document.getElementById('modal-country');
            const modalCategory = document.getElementById('modal-category');
            const modalResearch = document.getElementById('modal-research');
            const closeBtn = document.getElementsByClassName('close-btn')[0];
            
            // Close the modal when clicking the X
            closeBtn.onclick = function() {{
                modal.style.display = 'none';
            }};
            
            // Close the modal when clicking outside of it
            window.onclick = function(event) {{
                if (event.target == modal) {{
                    modal.style.display = 'none';
                }}
            }};
            
            // Close modal with Escape key
            document.addEventListener('keydown', function(event) {{
                if (event.key === 'Escape' && modal.style.display === 'block') {{
                    modal.style.display = 'none';
                }}
            }});
            
            // Create legend items
            const legendContainer = document.getElementById('legend-items');
            for (const category in legendData) {{
                const color = legendData[category];
                const item = document.createElement('div');
                item.className = 'legend-item';
                
                const colorBox = document.createElement('div');
                colorBox.className = 'color-box';
                colorBox.style.backgroundColor = color;
                
                const text = document.createElement('span');
                text.textContent = category;
                
                item.appendChild(colorBox);
                item.appendChild(text);
                legendContainer.appendChild(item);
                
                // Make legend items interactive - highlight related nodes
                item.style.cursor = 'pointer';
                item.addEventListener('mouseenter', function() {{
                    if (typeof network !== 'undefined') {{
                        const nodeIds = [];
                        Object.keys(nodeData).forEach(nodeId => {{
                            if (nodeData[nodeId].category === category) {{
                                nodeIds.push(nodeId);
                            }}
                        }});
                        
                        network.selectNodes(nodeIds);
                    }}
                }});
                
                item.addEventListener('mouseleave', function() {{
                    if (typeof network !== 'undefined') {{
                        network.unselectAll();
                    }}
                }});
            }}
            
            // Add click event to the network
            if (typeof network !== 'undefined') {{
                network.on('click', function(params) {{
                    if (params.nodes.length) {{
                        const nodeId = params.nodes[0];
                        const data = nodeData[nodeId];
                        
                        if (data) {{
                            modalTitle.textContent = data.potential_event;
                            modalDate.textContent = data.due_date;
                            modalCountry.textContent = data.research_country;
                            
                            // Set color for category based on legend
                            modalCategory.textContent = data.category;
                            const categoryColor = legendData[data.category];
                            if (categoryColor) {{
                                modalCategory.style.backgroundColor = categoryColor;
                                modalCategory.style.color = getContrastColor(categoryColor);
                            }}
                            
                            modalResearch.innerHTML = marked.parse(JSON.parse('"' + data.research + '"'));
                            modal.style.display = 'block';
                        }}
                    }}
                }});
                
                // Make nodes bigger on hover for better UX
                network.on('hoverNode', function(params) {{
                    network.canvas.body.container.style.cursor = 'pointer';
                }});
                
                network.on('blurNode', function(params) {{
                    network.canvas.body.container.style.cursor = 'default';
                }});
                
                console.log('Event handlers attached successfully');
            }} else {{
                console.error('Network object not available');
            }}
            
            // Helper function to determine text color based on background
            function getContrastColor(hexColor) {{
                // Convert hex to RGB
                let r = parseInt(hexColor.substr(1, 2), 16);
                let g = parseInt(hexColor.substr(3, 2), 16);
                let b = parseInt(hexColor.substr(5, 2), 16);
                
                // Calculate luminance
                let luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
                
                // Return black or white depending on background brightness
                return luminance > 0.5 ? '#000000' : '#ffffff';
            }}
            
        }} catch (error) {{
            console.error('Error initializing interactive elements:', error);
        }}
    }}, 1000); // Wait 1 second for network to initialize
}});
</script>
"""
