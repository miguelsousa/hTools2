# [h] hTools2.modules.anchors

"""Tools to create, move, delete and transfer anchors."""

# imports

from hTools2.modules.color import clear_colors, random_color

# font-level tools

def get_anchors(font, glyph_names=None):
    """Get all anchors in glyphs as a dictionary."""
    anchors_dict = {}
    if glyph_names == None:
        _glyph_names = font.keys()
    else:
        _glyph_names = glyph_names
    for glyph_name in _glyph_names:
        g = font[glyph_name]
        if len(g.anchors) > 0:
            anchors = []
            for a in g.anchors:
                anchors.append((a.name, a.position))
            anchors_dict[g.name] = anchors
    return anchors_dict

def clear_anchors(font, glyph_names=None):
    """Delete all anchors in font."""
    if glyph_names is None:
        glyph_names = font.keys()
    for glyph_name in glyph_names:
        if len(font[glyph_name].anchors) > 0:
            font[glyph_name].clearAnchors()
            font[glyph_name].update()
    font.update()

def find_lost_anchors(font):
    """Find anchors which are lost outside of the bounding box."""
    clear_colors(font)
    c = random_color()
    lost_anchors = []
    for g in font:
        if len(g.anchors) > 0:
            for a in g.anchors:
                if a.position[1] > f.info.unitsPerEm:
                    lost_anchors.append((g.name, a.name, a.position))
                    g.mark = c
    return lost_anchors

def remove_duplicate_anchors(font):
    """Delete duplicate anchors with same name and position."""
    # save existing anchors
    old_anchors = get_anchors(font)
    # collect clean anchors
    new_anchors = {}
    for glyph_name in old_anchors.keys():
        # glyphs with more than 1 anchor
        if len(old_anchors[glyph_name]) > 1:
            clean_anchors = []
            for i, a in enumerate(old_anchors[glyph_name]):
                if i == 0:
                    clean_anchors.append(a)
                    previous = a
                else:
                    # same name and pos: skip
                    if a[0] == previous[0]:
                        if a[1][0] == previous[1][0] and a[1][1] == previous[1][1]:
                            pass
                        else:
                            clean_anchors.append(a)
                previous = a
            # done glyph
            new_anchors[glyph_name] = clean_anchors
        # glyphs with only 1 anchor
        else:
            new_anchors[glyph_name] = old_anchors[glyph_name]
    # remove all anchors
    clear_anchors(font)
    # place new anchors
    for glyph_name in new_anchors.keys():
        for anchor in new_anchors[glyph_name]:
            name, pos = anchor
            font[glyph_name].appendAnchor(name, pos)
            font[glyph_name].update()
    # done

def get_anchors_dict(accents_dict):
    """Get an anchors dict from an accented glyphs dict."""
    # get anchors
    anchors_dict = {}
    for accented_glyph in accents_dict.keys():
        # get base glyph and accents
        base, accents = accents_dict[accented_glyph]
        # create entry
        if not anchors_dict.has_key(base):
            anchors_dict[base] = []
        # add anchor to lib
        for accent in accents:
            anchor_name = accent[1]
            if anchor_name not in anchors_dict[base]:
                anchors_dict[base].append(anchor_name)
    # done
    return anchors_dict

# glyph-level tools

def rename_anchor(glyph, old_name, new_name):
    """Rename anchors with name ``old_name`` in ``glyph`` to ``new_name``."""
    has_name = False
    if len(glyph.anchors) > 0:
        for a in glyph.anchors:
            if a.name == old_name:
                has_name = True
                a.name = new_name
                glyph.update()
    return has_name

def transfer_anchors(source_glyph, dest_glyph):
    """Transfer all anchors in ``source_glyph`` to ``dest_glyph``."""
    has_anchor = False
    if len(source_glyph.anchors) > 0 :
        # collect anchors in source glyph
        has_anchor = True
        anchorsDict = {}
        for a in source_glyph.anchors:
            anchorsDict[a.name] = a.position
        # clear anchors in dest glyph
        dest_glyph.clearAnchors()
        # place anchors in dest glyph
        for anchor in anchorsDict:
            dest_glyph.appendAnchor(anchor, anchorsDict[anchor])
            dest_glyph.update()
    # done
    return has_anchor

def move_anchors(glyph, anchor_names, (delta_x, delta_y)):
    """Move named anchors by ``(x,y)`` units."""
    for anchor in glyph.anchors:
        if anchor.name in anchor_names:
            anchor.move((delta_x, delta_y))
            glyph.update()

def create_anchors(glyph, top=True, bottom=True, accent=False, top_delta=20, bottom_delta=20):
    """Create ``top`` and ``bottom`` anchors at relative positions."""
    # make anchors list
    anchor_names = []
    if top:
        anchor_names.append('top')
    if bottom:
        anchor_names.append('bottom')
    # run
    font = glyph.getParent()
    has_anchor = False
    anchors = []
    # get existing anchors
    if len(glyph.anchors) > 0 :
        has_anchor = True
        for a in glyph.anchors:
            anchors.append(a.name)
    # add only new anchors
    x = glyph.width / 2
    for anchor_name in anchor_names:
        # add underscore if accent
        if accent:
            anchor_name = '_' + anchor_name
        if anchor_name not in anchors:
            # make anchor y-position
            if anchor_name in [ 'top', '_top' ]:
                y = font.info.xHeight + top_delta
            else:
                y = 0 - bottom_delta
            # place anchor
            glyph.appendAnchor(anchor_name, (x, y))
    # done glyph
    glyph.update()
