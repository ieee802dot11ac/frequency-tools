struct RndEntry {
    char filetype[];
    char filename[];
    bool unk;
};

struct RndFile {
    u32 ver;
    u32 entry_ct;
    RndEntry entries[entry_ct];
};

RndFile f @ 0x0;