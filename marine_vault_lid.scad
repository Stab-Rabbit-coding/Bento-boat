// Auto-generated Marine Vault LID V2 - External Fastener Tabs
$fn = 40;

module screw_tabs_lid() {
    // Main flat lid plate
    cube([161.2, 118.0, 4.0]);
    
    // Matching ears for the lid clearance bolts
        translate([-3.0, -10.0, 0]) cube([10.0, 10.0 + 1, 4.0]);
    translate([-3.0, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 4.0]);
    translate([26.4, -10.0, 0]) cube([10.0, 10.0 + 1, 4.0]);
    translate([26.4, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 4.0]);
    translate([55.8, -10.0, 0]) cube([10.0, 10.0 + 1, 4.0]);
    translate([55.8, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 4.0]);
    translate([85.19999999999999, -10.0, 0]) cube([10.0, 10.0 + 1, 4.0]);
    translate([85.19999999999999, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 4.0]);
    translate([154.2, -10.0, 0]) cube([10.0, 10.0 + 1, 4.0]);
    translate([154.2, 118.0 - 1, 0]) cube([10.0, 10.0 + 1, 4.0]);

}

module marine_vault_lid() {
    difference() {
        screw_tabs_lid();
        
        // Clearance Bolt Holes shifted outside the gasket boundary
                translate([2.0, -5.0, -1]) cylinder(r=1.7, h=6.0);
        translate([2.0, 118.0 + 4.0, -1]) cylinder(r=1.7, h=6.0);
        translate([31.4, -5.0, -1]) cylinder(r=1.7, h=6.0);
        translate([31.4, 118.0 + 4.0, -1]) cylinder(r=1.7, h=6.0);
        translate([60.8, -5.0, -1]) cylinder(r=1.7, h=6.0);
        translate([60.8, 118.0 + 4.0, -1]) cylinder(r=1.7, h=6.0);
        translate([90.19999999999999, -5.0, -1]) cylinder(r=1.7, h=6.0);
        translate([90.19999999999999, 118.0 + 4.0, -1]) cylinder(r=1.7, h=6.0);
        translate([159.2, -5.0, -1]) cylinder(r=1.7, h=6.0);
        translate([159.2, 118.0 + 4.0, -1]) cylinder(r=1.7, h=6.0);

    }
    
    // Inverted Knife-Edge Gasket Press Rails - Uninterrupted continuous grid
    translate([0, 0, 4.0]) {
                // Continuous Outer Knife-Edge Loop
        difference() {
            translate([1.2, 1.2, 0]) cube([158.79999999999998, 115.6, 2.4]);
            translate([2.8, 2.8, -1]) cube([155.6, 112.39999999999999, 2.4 + 2]);
        }
        translate([30.599999999999998, 4.0, 0]) cube([1.6, 110.0, 2.4]);
        translate([60.0, 4.0, 0]) cube([1.6, 110.0, 2.4]);
        translate([89.39999999999999, 4.0, 0]) cube([1.6, 110.0, 2.4]);

    }
}
marine_vault_lid();
