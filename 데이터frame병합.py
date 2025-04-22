df1 = pd.DataFrame([[1, 2, 'H', 10], [1, 2, 'I', 11], [3, 4, 'J', 12]],
                   columns=['A','B','C','G'])

df2 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                   columns=['D','E','F'])

df3 = pd.merge(df1, df2, left_on=['A', 'B'], right_on=['D','E'], how='inner')

df3.pivot(index=["A", "B"], columns="C", values="G").rename_axis(columns=None).reset_index()   # rename_axis(columns=None): 컬럼명을 변경하지 않음.
