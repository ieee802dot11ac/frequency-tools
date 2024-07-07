struct str_wrap {char a[];};
struct Rect {float b[4];};
struct Vector2{float x;float y;};
struct Trans {
    u32 ver;
    float local_xfm[12];
    float world_xfm[12];
    u32 trans_ct;
    str_wrap transes[trans_ct];
    u32 pad[4];
};
struct Draw {
    u32 ver;
    bool showing;
    u32 draw_ct;
    str_wrap draws[draw_ct];
};
struct Collide {
    u32 ver;
    u32 collide_ct;
    str_wrap collides[collide_ct];
};

struct Cam {
    u32 ver;
    Trans trans;
    Draw d;
    Collide col;
    float near_plane;
    float far_plane;
    float fov;
    Rect screen_rect;
    Vector2 z_range;
    bool target_tex_exists;
    if (target_tex_exists) {str_wrap target_tex;}
    float y_ratio;
};
Cam c @ 0;