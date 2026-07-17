// Auto-generated Marine Vault BASE V2 - External Fastener Tabs
$fn = 40; 

module screw_tabs_base() {
    // Main solid envelope
    cube([161.2, 118.0, 36.0]);
    
    // External structural tabs flanking the perimeter walls
        translate([-3.0, -10.0, 0]) cube([10.0, 10.0 + 1, 36.0]);
    translate([-3.0, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 36.0]);
    translate([26.4, -10.0, 0]) cube([10.0, 10.0 + 1, 36.0]);
    translate([26.4, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 36.0]);
    translate([55.8, -10.0, 0]) cube([10.0, 10.0 + 1, 36.0]);
    translate([55.8, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 36.0]);
    translate([85.19999999999999, -10.0, 0]) cube([10.0, 10.0 + 1, 36.0]);
    translate([85.19999999999999, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 36.0]);
    translate([154.2, -10.0, 0]) cube([10.0, 10.0 + 1, 36.0]);
    translate([154.2, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 36.0]);

}

module marine_vault_base() {
    difference() {
        screw_tabs_base();
        
        // Internal Chamber Cutouts
                translate([4.0, 4.0, 3.0]) cube([25.4, 110.0, 36.0]);
        translate([33.4, 4.0, 3.0]) cube([25.4, 110.0, 36.0]);
        translate([62.8, 4.0, 3.0]) cube([25.4, 110.0, 36.0]);
        translate([92.19999999999999, 4.0, 3.0]) cube([65.0, 110.0, 36.0]);

        
        // Aluminum Cooling Plate Inset
        translate([1.5, 1.5, -0.5]) 
            cube([158.2, 115.0, 3.5]);
            
        // Gasket Track System (Now completely uninterrupted by screw paths)
                // Perimeter Gasket Track (Shifted inward into wall core to clear external tabs)
        translate([0.8, 0.8, 36.0 - 3.0]) difference() {
            cube([159.6, 116.4, 3.0 + 1]);
            translate([2.4, 2.4, -1]) cube([154.79999999999998, 111.60000000000001, 3.0 + 3]);
        }
        translate([30.2, 4.0, 36.0 - 3.0]) cube([2.4, 110.0, 3.0 + 1]);
        translate([59.599999999999994, 4.0, 36.0 - 3.0]) cube([2.4, 110.0, 3.0 + 1]);
        translate([88.99999999999999, 4.0, 36.0 - 3.0]) cube([2.4, 110.0, 3.0 + 1]);

        
        // Stern Cable Glands
                translate([16.7, -1, 11.2]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([16.7, -1, 24.0]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([46.099999999999994, -1, 11.2]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([46.099999999999994, -1, 24.0]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([75.5, -1, 11.2]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([75.5, -1, 24.0]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([111.69999999999999, -1, 17.6]) rotate([-90, 0, 0]) cylinder(r=8.1, h=6.0);
        translate([137.7, -1, 17.6]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);

        
        // Heat-Set Insert Pilot Holes shifted completely into the external ears
                translate([2.0, -5.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);
        translate([2.0, 118.0 + 4.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);
        translate([31.4, -5.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);
        translate([31.4, 118.0 + 4.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);
        translate([60.8, -5.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);
        translate([60.8, 118.0 + 4.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);
        translate([90.19999999999999, -5.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);
        translate([90.19999999999999, 118.0 + 4.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);
        translate([159.2, -5.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);
        translate([159.2, 118.0 + 4.0, 31.0]) cylinder(r=2.1, h=5.0 + 1);

    }
}
marine_vault_base();
