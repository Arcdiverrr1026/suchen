ls = ["综合", "理工", "综合", "综合", "综合", "综合", "综合", "师范",
      "理工", "综合", "理工", "综合", "综合", "综合", "理工", "理工",
      "理工", "师范", "农林", "理工", "综合", "理工", "理工", "理工",
      "综合", "理工", "综合", "农林", "民族", "军事"]

school_types_count = {}

for school_type in ls:
    school_types_count[school_type] = school_types_count.get(school_type,0) + 1

for school_type in school_types_count:
    print("{}:{}".format(school_type,school_types_count[school_type]))