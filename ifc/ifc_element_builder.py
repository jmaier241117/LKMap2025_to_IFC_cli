import string

import ifcopenshell.guid

from ifcopenshell import file


def create_dsitribution_chamber_element(ifc_file: file, placement: any, productShapeDef: any, type: string) -> any:
    return ifc_file.createIfcDistributionChamberElement(ifcopenshell.guid.new(), None, 'Cylinder', None,
                                                        None, placement, productShapeDef, None, type)


def create_pipe_segment_element(ifc_file: file, placement: any, productShapeDef: any, type: string) -> any:
    return ifc_file.createIfcPipeSegment('2iirh2nx97a8aH1wk0tTo5', None, 'Pipe', None,
                                         None, placement, productShapeDef, None, type)


def create_chamber_element_placement(ifc_file: file, dimx: float, dimy: float) -> any:
    return ifc_file.createIfcLocalPlacement(cartesian_point_3d, ifc_file.createIfcAxis2Placement3D(
        ifc_file.createIfcCartesianPoint(
            (dimx, dimy, 0.0)),
        ifc_file.createIfcDirection((0.0, 0.0, -2.0)),
        ifc_file.createIfcDirection((1.0, 0.0, 0.0))))


def create_pipe_segment_placement(ifc_file: file, dimx: float, dimy: float) -> any:
    return ifc_file.createIfcLocalPlacement(cartesian_point_3d, ifc_file.createIfcAxis2Placement3D(
        ifc_file.createIfcCartesianPoint(
            (dimx, dimy, -2.0)),
        ifc_file.createIfcDirection((1.0, 0.0, 0.0)),
        ifc_file.createIfcDirection((0.0, 0.0, -1.0))))
