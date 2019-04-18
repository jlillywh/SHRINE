import hydrofunctions as hf


snake = hf.NWIS('13011000', 'dv', period='P55D')

snake.get_data()

print(snake.df().head())

print(snake.start_date)
print(snake.end_date)

