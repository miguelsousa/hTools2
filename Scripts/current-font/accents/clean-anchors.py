# [h] remove duplicate anchors

# debug

import hTools2.modules.anchors
reload(hTools2.modules.anchors)

# imports

from hTools2.modules.anchors import remove_duplicate_anchors

# run

f = CurrentFont()
remove_duplicate_anchors(f)
