import ezdxf

drawing = ezdxf.new(dxfversion='AC1024')  # or use the AutoCAD release name ezdxf.new(dxfversion='R2010')
modelspace = drawing.modelspace()
modelspace.add_line((0, 0), (10, 0), dxfattribs={'color': 7})
drawing.layers.new('TEXTLAYER', dxfattribs={'color': 2})
# use set_pos() for proper TEXT alignment - the relations between halign, valign, insert and align_point are tricky.
modelspace.add_text('Test', dxfattribs={'layer': 'TEXTLAYER'}).set_pos((0, 0.2), align='CENTER')
drawing.saveas('test.dxf')