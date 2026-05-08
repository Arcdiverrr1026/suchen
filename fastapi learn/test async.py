import asyncio

# 1. 定义异步函数
async def make_coffee():
    print("开始烧水...")
    # 2. 模拟耗时操作，await 会释放控制权
    await asyncio.sleep(2)
    print("咖啡泡好了！")
    return "热咖啡"

async def main():
    # 3. 必须 await 才能获取返回值
    coffee = await make_coffee()
    print(f"享用: {coffee}")

# 4. 运行顶层入口
asyncio.run(main())