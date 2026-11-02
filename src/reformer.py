"""Draw the demo illustration from original geometry in a single oblique projection."""

from math import cos, sin, pi


def project(v):
    x, y, z = v
    return f"{70 + 1.94*x + 1.26*y:.1f},{370 - .67*x + .69*y - 1.57*z:.1f}"


def polygon(points, fill):
    return f'<polygon points="{" ".join(map(project, points))}" fill="{fill}"/>'


def line(start, end, color, width=1):
    return f'<path d="M{project(start)} L{project(end)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'


def box(x, y, z, length, width, height, colors):
    a,b,c = x+length, y+width, z+height
    return ''.join([
        polygon([(x,y,z),(x,b,z),(x,b,c),(x,y,c)], colors[0]),
        polygon([(x,b,z),(a,b,z),(a,b,c),(x,b,c)], colors[1]),
        polygon([(x,y,c),(a,y,c),(a,b,c),(x,b,c)], colors[2])
    ])


def cushion(x, y, z, length, width, height, radius, colors):
    points = []
    for cx, cy, angle in [(x+radius,y+radius,180),(x+length-radius,y+radius,270),
                           (x+length-radius,y+width-radius,0),(x+radius,y+width-radius,90)]:
        for i in range(7):
            a = (angle + i*15) * pi / 180
            points.append((cx+radius*cos(a),cy+radius*sin(a)))
    bottom = [(a,b,z) for a,b in points]
    top = [(a,b,z+height) for a,b in points]
    # Draw the extrusion before the top and a thin piping seam.
    chunks = [polygon(bottom, colors[0])]
    for i in range(len(points)):
        j=(i+1) % len(points)
        chunks.append(polygon([bottom[i],bottom[j],top[j],top[i]],colors[0]))
    rim = " ".join(map(project,top))
    chunks += [polygon(top,colors[1]), f'<polygon points="{rim}" fill="none" stroke="{colors[2]}" stroke-width=".9"/>']
    return ''.join(chunks)


def illustration():
    wood = ('#a7794b','#bf9868','#e9c99d')
    steel = ('#6c7d7e','#a4aeaa','#d6dfd6')
    leather = ('#243e4b','#42606c','#768a8c')
    parts = ['''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 710 510" role="img" aria-label="Иллюстрация реформера. Деревянная рама, подвижная каретка, тросы и регулируемый упор.">
      <defs><pattern id="hp-grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#3b5753" stroke-opacity=".11" stroke-width=".8"/></pattern>
      <filter id="hp-soft" x="-40%" y="-100%" width="180%" height="300%"><feGaussianBlur stdDeviation="8"/></filter>
      <linearGradient id="hp-field" x2=".7" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="#eceddf"/><stop offset="1" stop-color="#d4dcce"/></linearGradient></defs>
      <rect width="710" height="510" fill="url(#hp-field)"/><rect width="710" height="510" fill="url(#hp-grid)"/>''']
    parts.append('<g transform="translate(9 -9)">')
    parts.append('<g filter="url(#hp-soft)" opacity=".18">'+polygon([(-4,-5,0),(265,-5,0),(275,87,0),(-4,87,0)],'#3b483d')+'</g>')
    for x in (7,241):
        for y in (3,66):
            parts.append(box(x,y,0,11,10,21,wood))
            parts.append(box(x,y,0,11,10,2,steel))
    parts.append(box(0,0,15,262,79,5,wood))
    parts.append(box(4,4,20,254,70,1,('#53625a',)*3))
    parts.append(box(0,0,19,262,5,13,wood))
    for y in (7,69):
        parts.append(box(5,y,27,249,3,3,steel))
    parts.append(box(251,0,19,11,79,13,wood))
    parts.append(box(2,5,24,12,68,5,steel))
    # Five wound springs attach the carriage to the foot end.
    for y in (18,28,38,48,58):
        parts.append(line((12,y,27),(64,y,27),'#7b8982',1.4))
        coils=[(19+i*.72,y+1.35*cos(i*pi/2),27+1.35*sin(i*pi/2)) for i in range(52)]
        parts.append(f'<polyline points="{" ".join(map(project,coils))}" fill="none" stroke="#737e76" stroke-width="1.2"/>')
    for y in (10,63):
        parts.append(box(243,y,31,5,5,43,steel))
        px,py=project((245,y+3,74)).split(',')
        parts.append(f'<circle cx="{px}" cy="{py}" r="6.5" fill="#354b4c"/><circle cx="{px}" cy="{py}" r="2.6" fill="#c6c9b8"/>')
    parts.append(cushion(58,6,31,139,67,6,5,leather))
    parts.append(cushion(194,23,31,33,32,7,4,leather))
    for y in (12,55):
        parts.append(cushion(177,y,37,13,11,13,4,leather))
    for y in (0,78):
        inner = 18 if y==0 else 59
        parts.append(line((245,10 if y==0 else 66,74),(174,inner,52),'#405354',1.9))
        px,py=project((169,inner,51)).split(',')
        parts.append(f'<ellipse cx="{px}" cy="{py}" rx="12" ry="4.2" transform="rotate(-20 {px} {py})" fill="none" stroke="#465c5b" stroke-width="3.1"/>')
    parts.append(box(0,74,19,262,5,13,wood))
    for i in range(5):
        parts.append(line((5+i*2,79,20+i*2),(254-i*3,79,20+i*2),'#aa865d',.5))
    parts.append(box(0,0,19,5,79,13,wood))
    parts.append(cushion(1,6,32,12,66,3,2,leather))
    # Raised footbar with curved corners and a padded central grip.
    for y in (5,73):
        parts.append(line((27,y,29),(12,y,65),'#778b89',5.5))
        parts.append(line((27,y,29),(12,y,65),'#c4d0c6',2))
        parts.append(line((35,y,30),(18,y,53),'#879a95',3.5))
    parts.append(line((12,5,65),(12,73,65),'#738681',7))
    parts.append(line((12,10,65),(12,68,65),'#344c56',10))
    for x in (6,24,240,255):
        px,py=project((x,79.2,26)).split(',')
        parts.append(f'<circle cx="{px}" cy="{py}" r="1.7" fill="#786b53"/>')
    parts.append('''</g><g fill="none" stroke="#3f5b55" stroke-width="1" opacity=".7"><path d="M301 266v-77l-35-22h-52"/><circle cx="301" cy="266" r="3" fill="#d6ddce"/><path d="M151 310l-41-38H63"/><circle cx="151" cy="310" r="3" fill="#d6ddce"/><path d="M532 205l42 40h66"/><circle cx="532" cy="205" r="3" fill="#d6ddce"/></g>
    <g fill="#38524c" font-family="Arial, sans-serif" font-size="13" letter-spacing="1"><text x="214" y="159">01</text><text x="63" y="265">02</text><text x="620" y="238">03</text></g></svg>''')
    return ''.join(parts)
