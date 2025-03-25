from string import whitespace
from base64 import b64decode
import re
import json
from web.modal_js import modal_js_template
import os

def whitespaces_to_line_breaks(string: str, each_num: int = 5) -> str:
    indexes = [i for i, char in enumerate(string) if char in whitespace]

    indexes = indexes[each_num-1::each_num]

    for index in indexes:
        string = string[:index] + "\n" + string[index + 1:]

    return string

def options_setting(network):
    # Set options
    options = {
        "edges": {
            "arrows": {
                "to": {
                    "enabled": True,
                    "scaleFactor": 1,
                }
            },
            "smooth": {
                "enabled": True,
                "type": "cubeBezier",
                "roundness": 0.5,
            },
            "font": {
                "size": 14,
                "color": "#343434",
                "face": "Inter, sans-serif",
                "background": "rgba(255, 255, 255, 0.8)",
                "strokeWidth": 0,
                "align": "middle",
            }
        },
        "physics": {
            "enabled": False,
        },
        "nodes": {
            "font": {
                "size": 16,
                "face": "Inter, sans-serif",
                "color": "#333333",
            },
            "shape": "box",
            "margin": 12,
            "borderWidth": 1,
            "borderWidthSelected": 2,
            "shadow": True,
        }
    }

    # Set the options
    network.set_options(json.dumps(options))

def create_graph_structure_and_legend(data, color_map, categories):
    # Create a simplified data structure for the nodes
    node_info = {}
    for item in data:
        node_id = str(item["_id"])
        content = b64decode(item["research"].encode()).decode()
        content = re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL)

        content = re.sub(r'\s*?\n', '<br>', content)
        content = re.sub(r'---<br>', r'<hr>', content)

        content = re.sub(r'#####\s(.*?)<br>', r'<h5>\1</h5>', content)
        content = re.sub(r'####\s(.*?)<br>', r'<h4>\1</h4>', content)
        content = re.sub(r'###\s(.*?)<br>', r'<h3>\1</h3>', content)
        content = re.sub(r'##\s(.*?)<br>', r'<h2>\1</h2>', content)
        content = re.sub(r'#\s(.*?)<br>', r'<h1>\1</h1>', content)

        # Replace "..." with “...”
        content = re.sub(r'"(.*?)"', '\u201c\\1\u201d', content)

        node_info[node_id] = {
            "research_country": item["research_country"],
            "research_date": item["research_date"],
            "potential_event": item["potential_event"],
            "category": item["category"],
            "research": content,
        }

    # Also prepare a legend for categories
    legend_data = {category: color_map[category] for category in categories}

    return legend_data, node_info

def get_final_html(network, graph, color_map, legend_data, node_info, file_path="graph.html"):
    network.save_graph(file_path)

    # Update node colors based on category
    for node in network.nodes:
        node_id = node['id']
        if 'category' in graph.nodes[node_id]:
            node['color'] = color_map[graph.nodes[node_id]['category']]

            # Check if file exists and has content
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r', encoding='utf-8') as file:
                    source_code = file.read()

                    # Find where to insert our custom code
                    head_end_index = source_code.find('</head>')
                    body_end_index = source_code.find('</body>')

                    if head_end_index != -1 and body_end_index != -1:
                        # JSON.stringify the node data, and escape it properly
                        node_data_json = json.dumps(node_info)
                        node_data_json = node_data_json.replace('\\', '\\\\').replace("'", "\\'")

                        # JSON for the legend
                        legend_json = json.dumps(legend_data)
                        legend_json = legend_json.replace('\\', '\\\\').replace("'", "\\'")

                        # The modal and legend - improved styling, layout, UX
                        with open("web/modal.css", "r") as file:
                            modal_css: str = f"<style>{file.read()}</style>"
                        with open("web/modal.html", "r") as file:
                            modal_html: str = file.read()
                        modal_js: str = modal_js_template.format(node_data_json=node_data_json, legend_json=legend_json)

                        # Insert CSS in head
                        head_part = source_code[:head_end_index] + modal_css + source_code[
                                                                               head_end_index:body_end_index]

                        # Insert HTML and JS before body end
                        final_html = head_part + modal_html + modal_js + source_code[body_end_index:]

                        return final_html
                    else:
                        return "Error: Could not locate insertion points in the HTML"
            else:
                return "Error: Graph file is empty or doesn't exist"
