import pandas as pd 

df = pd.DataFrame( [ [1, 1, 1], [2, 2, 2] ], columns=['a', 'b', 'c'])

df.to_csv('s3://dash-test-bucket-567-open/dummy.csv', index=False)


# import s3fs
# fs = s3fs.S3FileSystem(anon=True)
# fs.ls('dash-test-bucket-567-open')
# # ['my-file.txt']
# # with fs.open('my-bucket/my-file.txt', 'rb') as f:
# #     print(f.read())
pd.__version__

