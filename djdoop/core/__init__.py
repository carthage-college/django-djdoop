PROFILED_PAIRS = """
SELECT cc_stage_merge_no, prim_id, sec_id, id1, id2,
fullname1, fullname2, ofc_add_by1, ofc_add_by2, add_date1, add_date2, upd_date1, upd_date2,
id1_com, id2_com, id1_adm, id2_adm, id1_dev, id2_dev, id1_fa, id2_fa, id1_fin, id2_fin, id1_hr, id2_hr, id1_mat, id2_mat, id1_reg, id2_reg, id1_stu, id2_stu,
merge_status
FROM cc_stage_merge
WHERE profile_date is not null
"""
