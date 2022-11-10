from gpbp_osm import layers, data_src


def test_init_admarea():
    adm_area = layers.AdmArea("GRC", level=0)
    assert adm_area is not None


def test_world_pop():
    adm_area = layers.AdmArea("GRC", level=0)
    adm_area.get_adm_area("Greece")
    df = data_src.world_pop_data(adm_area=adm_area)
    est_pop = round(df["population"].sum() / 1000000, 1)
    print(est_pop)
    assert est_pop == 10.4


def test_fb_pop():
    adm_area = layers.AdmArea("GRC", level=0)
    adm_area.get_adm_area("Greece")
    df = data_src.fb_pop_data(adm_area=adm_area)
    est_pop = round(df["population"].sum() / 1000000, 1)
    print(est_pop)
    assert est_pop == 10.4
