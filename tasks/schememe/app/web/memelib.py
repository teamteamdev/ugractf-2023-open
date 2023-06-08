import lxml.etree as ET

font_declaration = '''
<font id="impact" horiz-adv-x="1000">
  <font-face font-family="Impact" units-per-em="2048" ascent="1946" descent="102" >
    <font-face-src>
      <font-face-name name="Impact" />
    </font-face-src>
  </font-face>
</font>
'''

style_string = b'fill:#FFFFFF;fill-opacity:1;stroke:#000000;stroke-width:0.3px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;'

def create_error(error_code):
    error_svg_declaration = '''
    <svg xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://www.w3.org/2000/svg" sodipodi:docname="stop.svg" viewBox="0 0 300 300" version="1.1" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" inkscape:version="0.91 r13725" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd">
      <sodipodi:namedview fit-margin-left="0" inkscape:zoom="2.4814454" borderopacity="1" inkscape:current-layer="svg2" inkscape:cx="186.06297" inkscape:cy="160.48929" inkscape:window-maximized="1" showgrid="false" fit-margin-right="0" bordercolor="#666666" inkscape:window-x="0" guidetolerance="10" objecttolerance="10" inkscape:window-y="24" fit-margin-bottom="0" inkscape:window-width="1920" inkscape:pageopacity="0" inkscape:pageshadow="2" pagecolor="#ffffff" gridtolerance="10" inkscape:window-height="1056" fit-margin-top="0"/>
      <g fill-rule="evenodd">
        <path d="m211.2 297.2-122.1-0.1-86.34-86.4 0.061-122 86.38-86.35 122.1 0.058 86.3 86.37-0.1 122.1z" inkscape:transform-center-x="-6.3569551" inkscape:transform-center-y="-9.6240104" inkscape:connector-curvature="0" stroke="#c00" stroke-linecap="round" stroke-width="5.171" sodipodi:nodetypes="ccccccccc" fill="#fff"/>
        <path d="m203.9 279.8-107.7-0.0496-76.1-76.17 0.04961-107.7 76.17-76.1 107.7 0.04959 76.1 76.17-0.0496 107.7z" inkscape:transform-center-x="-5.6060084" inkscape:transform-center-y="-8.4871386" inkscape:connector-curvature="0" sodipodi:nodetypes="ccccccccc" fill="#c00"/>
      </g>
      <g fill-rule="evenodd" fill="#fff" transform="matrix(.5605 0 0 .5605 -2.306 1.266)">
        <path d="m276.4 245.1c52.25 0 82.61 64.34 82.61 116.6 0 52.25-52.36 80.61-104.6 80.61-52.25 0-92.61-42.36-92.61-94.61s42.36-102.6 94.61-102.6" sodipodi:nodetypes="csssc" inkscape:connector-curvature="0"/>
        <g stroke="#fff" stroke-linecap="round" stroke-width="48">
        <path d="m185.8 158v190" sodipodi:nodetypes="cc" inkscape:connector-curvature="0"/>
        <path d="m236.3 124.1v190" sodipodi:nodetypes="cc" inkscape:connector-curvature="0"/>
        <path d="m286.9 98.2v190" sodipodi:nodetypes="cc" inkscape:connector-curvature="0"/>
        <path d="m337.4 129.5v190" sodipodi:nodetypes="cc" inkscape:connector-curvature="0"/>
        <path d="m422.9 269.3-88.67 107.9-9.037 11" sodipodi:nodetypes="ccc" inkscape:connector-curvature="0"/>
        </g>
      </g>
    </svg>
    '''
    error_svg = ET.fromstring(error_svg_declaration)
    font_node = ET.fromstring(font_declaration)
    error_svg.append(font_node)
    bottom_text_node = ET.Element("text")
    bottom_text_node.text = f"ОШИБКА 0х0000000{error_code}"
    bottom_text_node.attrib['x'] = b'50%'
    bottom_text_node.attrib['y'] = b'90%'
    bottom_text_node.attrib['text-anchor'] = b'middle'
    bottom_text_node.attrib['font-size'] = b'1em'
    bottom_text_node.attrib['font-family'] = b'Impact'
    bottom_text_node.attrib['style'] = style_string
    error_svg.append(bottom_text_node)
    result = ET.tostring(error_svg).decode('utf-8')
    return result

def create_meme(svg_source, upper_text=None, bottom_text=None):
    if upper_text is None and bottom_text is None:
        return ET.tostring(svg_source)
    
    new_svg = svg_source

    font_node = ET.fromstring(font_declaration)
    new_svg.append(font_node)

    if upper_text is not None:
        upper_text_node = ET.Element("text")
        upper_text_node.text = upper_text
        upper_text_node.attrib['x'] = b'50%'
        upper_text_node.attrib['y'] = b'10%'
        upper_text_node.attrib['text-anchor'] = b'middle'
        upper_text_node.attrib['font-size'] = b'0.5em'
        upper_text_node.attrib['font-family'] = b'Impact'
        upper_text_node.attrib['style'] = style_string
        new_svg.append(upper_text_node)
    
    if bottom_text is not None:
        bottom_text_node = ET.Element("text")
        bottom_text_node.text = bottom_text
        bottom_text_node.attrib['x'] = b'50%'
        bottom_text_node.attrib['y'] = b'90%'
        bottom_text_node.attrib['text-anchor'] = b'middle'
        bottom_text_node.attrib['font-size'] = b'0.5em'
        bottom_text_node.attrib['font-family'] = b'Impact'
        bottom_text_node.attrib['style'] = style_string
        new_svg.append(bottom_text_node)

    result = ET.tostring(new_svg).decode('utf-8')
    return result