# -*- coding: utf-8 -*-

"""Test views."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import numpy as np
from numpy.testing import assert_allclose as ac
from vispy.util import keys

from phy.electrode.mea import staggered_positions
from phy.gui import GUI
from phy.io.mock import artificial_waveforms
from phy.utils import Bunch

from ..waveform import WaveformView


#------------------------------------------------------------------------------
# Test waveform view
#------------------------------------------------------------------------------

def test_waveform_view(qtbot):
    nc = 5

    def get_waveforms(cluster_id):
        return Bunch(data=artificial_waveforms(10, 20, nc),
                     channel_ids=np.arange(nc),
                     )

    channel_positions = staggered_positions(nc)

    v = WaveformView(waveforms=get_waveforms,
                     channel_positions=channel_positions,
                     )
    gui = GUI()
    gui.show()
    v.attach(gui)
    qtbot.addWidget(gui)

    # qtbot.waitForWindowShown(gui)

    v.on_select([])
    v.on_select([0])
    v.on_select([0, 2, 3])
    v.on_select([0, 2])

    v.toggle_waveform_overlap()
    v.toggle_waveform_overlap()

    v.toggle_zoom_on_channels()
    v.toggle_zoom_on_channels()

    v.toggle_show_labels()
    v.toggle_show_labels()

    # Box scaling.
    bs = v.boxed.box_size
    v.increase()
    v.decrease()
    ac(v.boxed.box_size, bs)

    bs = v.boxed.box_size
    v.widen()
    v.narrow()
    ac(v.boxed.box_size, bs)

    # Probe scaling.
    bp = v.boxed.box_pos
    v.extend_horizontally()
    v.shrink_horizontally()
    ac(v.boxed.box_pos, bp)

    bp = v.boxed.box_pos
    v.extend_vertically()
    v.shrink_vertically()
    ac(v.boxed.box_pos, bp)

    a, b = v.probe_scaling
    v.probe_scaling = (a, b * 2)
    ac(v.probe_scaling, (a, b * 2))

    a, b = v.box_scaling
    v.box_scaling = (a * 2, b)
    ac(v.box_scaling, (a * 2, b))

    v.zoom_on_channels([0, 2, 4])

    # Simulate channel selection.
    _clicked = []

    @v.gui.connect_
    def on_channel_click(channel_idx=None, button=None, key=None):
        _clicked.append((channel_idx, button, key))

    v.events.key_press(key=keys.Key('2'))
    v.events.mouse_press(pos=(0., 0.), button=1)
    v.events.key_release(key=keys.Key('2'))

    assert _clicked == [(0, 1, 2)]

    # qtbot.stop()
    gui.close()
