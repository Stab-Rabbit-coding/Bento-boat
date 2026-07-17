import argparse
import os

def generate_marine_vault_system_v3(args):
    # --- PARSE AND CALCULATE CORE GEOMETRY ---
    wall_thick = args.wall_thickness
    inner_height = args.height
    
    # Chamber lengths dynamic mapping
    # Generates an array of individual internal X-axis lengths
    ch_lengths = ([args.small_len] * args.small_count) + ([args.large_len] * args.large_count)
    total_chambers = len(ch_lengths)
    
    if total_chambers == 0:
        print("Error: You must specify at least 1 small or 1 large chamber.")
        return

    inner_width = args.width
    
    # Gasket Profile
    groove_w = 2.4          
    groove_d = 3.0          
    knife_w = 1.6           
    knife_h = 2.4           
    
    # Aluminum Cooling Plate Inset
    plate_thick = 3.0       
    lip_width = 2.5         
    
    # Screw Boss Tabs
    tab_size = 10.0         
    
    # Computed structural math
    total_inner_length = sum(ch_lengths) + (total_chambers - 1) * wall_thick
    outer_length = total_inner_length + (2 * wall_thick)
    outer_width = inner_width + (2 * wall_thick)
    outer_height = inner_height + wall_thick

    # =========================================================================
    # 1. GENERATE DYNAMIC BASE SCAD
    # =========================================================================
    base_scad = f"""// Auto-generated Flexible Marine Vault BASE V3
// Config: {args.small_count}x Small ({args.small_len}mm), {args.large_count}x Large ({args.large_len}mm)
$fn = 40; 

module screw_tabs_base() {{
    cube([{outer_length}, {outer_width}, {outer_height}]);
    {generate_external_tabs(ch_lengths, wall_thick, outer_width, outer_height, tab_size)}
}}

module marine_vault_base() {{
    difference() {{
        screw_tabs_base();
        
        // Internal Chamber Cutouts
        {generate_chamber_cutouts(ch_lengths, wall_thick, inner_width, outer_height)}
        
        // Aluminum Cooling Plate Inset
        translate([{wall_thick - lip_width}, {wall_thick - lip_width}, -0.5]) 
            cube([{total_inner_length + (2 * lip_width)}, {inner_width + (2 * lip_width)}, {plate_thick + 0.5}]);
            
        // Gasket Track System
        {generate_uninterrupted_gasket_grooves(ch_lengths, wall_thick, inner_width, outer_height, groove_w, groove_d)}
        
        // Dynamic Cable Glands
        {generate_dynamic_cable_glands(ch_lengths, wall_thick, inner_width, inner_height, args)}
        
        // Fastener Pilot Holes
        {generate_tab_fastener_holes(ch_lengths, wall_thick, outer_width, outer_height, tab_size)}
    }}
}}
marine_vault_base();
"""

    # =========================================================================
    # 2. GENERATE DYNAMIC LID SCAD
    # =========================================================================
    lid_scad = f"""// Auto-generated Flexible Marine Vault LID V3
$fn = 40;

module screw_tabs_lid() {{
    cube([{outer_length}, {outer_width}, {wall_thick}]);
    {generate_external_tabs(ch_lengths, wall_thick, outer_width, wall_thick, tab_size)}
}}

module marine_vault_lid() {{
    difference() {{
        screw_tabs_lid();
        {generate_lid_tab_screw_holes(ch_lengths, wall_thick, outer_width, tab_size)}
    }}
    
    translate([0, 0, {wall_thick}]) {{
        {generate_uninterrupted_lid_knife_edges(ch_lengths, wall_thick, inner_width, groove_w, knife_w, knife_h)}
    }}
}}
marine_vault_lid();
"""

    with open("marine_vault_base.scad", "w") as f:
        f.write(base_scad)
    with open("marine_vault_lid.scad", "w") as f:
        f.write(lid_scad)
        
    print(f"\n[Success] Generated geometry files for a {total_chambers}-SBC Cluster:")
    print(f" -> Base Enclosure:  marine_vault_base.scad ({outer_length:.1f}mm x {outer_width:.1f}mm)")
    print(f" -> Compression Lid: marine_vault_lid.scad")


# --- CAD Engine Subroutines ---

def generate_external_tabs(lengths, wall, out_width, height, t_size):
    code = ""
    current_x = wall / 2 - t_size / 2
    for length in lengths:
        code += f"    translate([{current_x}, -{t_size}, 0]) cube([{t_size}, {t_size} + 0.1, {height}]);\n"
        code += f"    translate([{current_x}, {out_width} - 0.1, 0]) cube([{t_size}, {t_size} + 0.1, {height}]);\n"
        current_x += length + wall
    code += f"    translate([{current_x}, -{t_size}, 0]) cube([{t_size}, {t_size} + 0.1, {height}]);\n"
    code += f"    translate([{current_x}, {out_width} - 0.1, 0]) cube([{t_size}, {t_size} + 0.1, {height}]);\n"
    return code

def generate_chamber_cutouts(lengths, wall, width, total_h):
    code = ""
    current_x = wall
    for length in lengths:
        code += f"        translate([{current_x}, {wall}, 3.0]) cube([{length}, {width}, {total_h}]);\n"
        current_x += length + wall
    return code

def generate_uninterrupted_gasket_grooves(lengths, wall, width, out_height, g_w, g_d):
    code = "        // Continuous Track Loops\n"
    g_offset = (wall / 2) - (g_w / 2)
    code += f"        translate([{g_offset}, {g_offset}, {out_height} - {g_d}]) difference() {{\n"
    code += f"            cube([{sum(lengths) + wall * len(lengths) + wall - 2*g_offset}, {width + 2*wall - 2*g_offset}, {g_d} + 1]);\n"
    code += f"            translate([{g_w}, {g_w}, -1]) cube([{sum(lengths) + wall * len(lengths) + wall - 2*g_offset - 2*g_w}, {width + 2*wall - 2*g_offset - 2*g_w}, {g_d} + 3]);\n"
    code += f"        }}\n"
    
    current_x = wall
    for length in lengths[:-1]:
        current_x += length
        code += f"        translate([{current_x + wall/2 - g_w/2}, {wall}, {out_height} - {g_d}]) cube([{g_w}, {width}, {g_d} + 1]);\n"
        current_x += wall
    return code

def generate_uninterrupted_lid_knife_edges(lengths, wall, width, g_w, k_w, k_h):
    track_center_offset = wall / 2
    edge_start = track_center_offset - (k_w / 2)
    code = ""
    code += f"        difference() {{\n"
    code += f"            translate([{edge_start}, {edge_start}, 0]) cube([{sum(lengths) + wall * len(lengths) + wall - 2*edge_start}, {width + 2*wall - 2*edge_start}, {k_h}]);\n"
    code += f"            translate([{edge_start + k_w}, {edge_start + k_w}, -1]) cube([{sum(lengths) + wall * len(lengths) + wall - 2*edge_start - 2*k_w}, {width + 2*wall - 2*edge_start - 2*k_w}, {k_h} + 2]);\n"
    code += f"        }}\n"
    
    current_x = wall
    for length in lengths[:-1]:
        current_x += length
        code += f"        translate([{current_x + wall/2 - k_w/2}, {wall}, 0]) cube([{k_w}, {width}, {k_h}]);\n"
        current_x += wall
    return code

def generate_dynamic_cable_glands(lengths, wall, width, height, args):
    code = "        // Dynamic Directional Cable Glands\n"
    gland_r = 6.1 if args.gland_type.upper() == "M12" else 8.1
    current_x = wall
    
    for i, length in enumerate(lengths):
        center_x = current_x + (length / 2)
        
        # PORT SIDE DRILLING (Y = wall face)
        if args.gland_side.lower() in ["port", "both"]:
            if args.gland_count == 1:
                code += f"        translate([{center_x}, -1, {height * 0.5}]) rotate([-90, 0, 0]) cylinder(r={gland_r}, h={wall + 2});\n"
            elif args.gland_count == 2:
                code += f"        translate([{center_x}, -1, {height * 0.35}]) rotate([-90, 0, 0]) cylinder(r={gland_r}, h={wall + 2});\n"
                code += f"        translate([{center_x}, -1, {height * 0.75}]) rotate([-90, 0, 0]) cylinder(r={gland_r}, h={wall + 2});\n"
                
        # STARBOARD SIDE DRILLING (Y = width face)
        if args.gland_side.lower() in ["starboard", "both"]:
            if args.gland_count == 1:
                code += f"        translate([{center_x}, {width + wall - 1}, {height * 0.5}]) rotate([-90, 0, 0]) cylinder(r={gland_r}, h={wall + 2});\n"
            elif args.gland_count == 2:
                code += f"        translate([{center_x}, {width + wall - 1}, {height * 0.35}]) rotate([-90, 0, 0]) cylinder(r={gland_r}, h={wall + 2});\n"
                code += f"        translate([{center_x}, {width + wall - 1}, {height * 0.75}]) rotate([-90, 0, 0]) cylinder(r={gland_r}, h={wall + 2});\n"
                
        current_x += length + wall
    return code

def generate_tab_fastener_holes(lengths, wall, out_width, out_height, t_size):
    code = ""
    hole_r = 2.1 
    hole_d = 5.0
    z_pos = out_height - hole_d
    
    current_x = wall / 2
    for length in lengths:
        code += f"        translate([{current_x}, -{t_size / 2}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
        code += f"        translate([{current_x}, {out_width} + {t_size / 2 - 1}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
        current_x += length + wall
    code += f"        translate([{current_x}, -{t_size / 2}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
    code += f"        translate([{current_x}, {out_width} + {t_size / 2 - 1}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
    return code

def generate_lid_tab_screw_holes(lengths, wall, out_width, t_size):
    code = ""
    bolt_r = 1.7 
    current_x = wall / 2
    for length in lengths:
        code += f"        translate([{current_x}, -{t_size / 2}, -1]) cylinder(r={bolt_r}, h={wall + 2});\n"
        code += f"        translate([{current_x}, {out_width} + {t_size / 2 - 1}, -1]) cylinder(r={bolt_r}, h={wall + 2});\n"
        current_x += length + wall
    code += f"        translate([{current_x}, -{t_size / 2}, -1]) cylinder(r={bolt_r}, h={wall + 2});\n"
    code += f"        translate([{current_x}, {out_width} + {t_size / 2 - 1}, -1]) cylinder(r={bolt_r}, h={wall + 2});\n"
    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parametric IP67 Marine Compute Vault CLI Engine")
    
    # Structural Clusters
    parser.add_init = parser.add_argument_group('Chamber Matrix Options')
    parser.add_init.add_argument('--small-count', type=int, default=3, help='Number of small node blades (e.g., Picos, PocketBeagles)')
    parser.add_init.add_argument('--small-len', type=float, default=25.4, help='Internal X length of small chamber (mm)')
    parser.add_init.add_argument('--large-count', type=int, default=1, help='Number of large master nodes (e.g., RPi 4B, BeagleBone Blue)')
    parser.add_init.add_argument('--large-len', type=float, default=65.0, help='Internal X length of large chamber (mm)')
    
    # Internal Envelope
    parser.add_init.add_argument('--width', type=float, default=110.0, help='Total baseline interior clearance width (mm)')
    parser.add_init.add_argument('--height', type=float, default=32.0, help='Interior structural z-depth clearance (mm)')
    parser.add_init.add_argument('--wall-thickness', type=float, default=4.0, help='CF-PETG shell wall width (mm)')
    
    # Marine Cable Routing
    parser.add_init.add_argument('--gland-side', type=str, default='port', choices=['port', 'starboard', 'both'], help='Enclosure face where glands exit')
    parser.add_init.add_argument('--gland-count', type=int, default=2, choices=[1, 2], help='Number of vertical glands per single chamber module')
    parser.add_init.add_argument('--gland-type', type=str, default='M12', choices=['M12', 'M16'], help='Thread rating size for marine glands')

    args = parser.parse_args()
    generate_marine_vault_system_v3(args)