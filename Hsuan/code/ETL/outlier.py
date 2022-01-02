data["PM2.5"].describe()

Upper_boundary_limit = Dayuan["PM2.5"].mean() + 3* Dayuan["PM2.5"].std()
Lower_boundary_limit = Dayuan["PM2.5"].mean() - 3* Dayuan["PM2.5"].std()

Upper_boundary_limit, Lower_boundary_limit

IQR = Dayuan["PM2.5"].quantile(0.75) - Dayuan["PM2.5"].quantile(0.25)

Lower_quantile_lower = Dayuan["PM2.5"].quantile(0.25) - (IQR * 1.5)
Upper_quantile_lower = Dayuan["PM2.5"].quantile(0.75) + (IQR * 1.5)

Upper_quantile_lower, Lower_quantile_lower, IQR

data[(data["PM2.5"]<Lower_boundary_limit)|(data["PM2.5"]>Upper_boundary_limit)]


Da = data[data["Station"] == "大園"]

a = Da[Da["PM2.5"] == 1000]

data = merge_df[merge_df.Date >= datetime.strptime("2019-01-01", "%Y-%m-%d")].sort_values(by = "Date")

a = Da[Da.Date >= datetime.strptime("2020-04-12", "%Y-%m-%d")]

Dayuan[Dayuan["PM2.5"] > 200]
