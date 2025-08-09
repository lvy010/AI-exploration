# OpenAI API密钥设置指南

## 方法1：环境变量设置（推荐）

### Linux/Mac系统
```bash
# 临时设置（当前会话有效）
export OPENAI_API_KEY="your-api-key-here"

# 永久设置（添加到bashrc）
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Windows系统
```cmd
# 临时设置
set OPENAI_API_KEY=your-api-key-here

# 永久设置（系统环境变量）
# 1. 右键"此电脑" -> 属性 -> 高级系统设置 -> 环境变量
# 2. 在"用户变量"中新建 OPENAI_API_KEY
# 3. 值设为 your-api-key-here
```

## 方法2：Python代码中设置

在Python代码开头添加：
```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

## 方法3：.env文件设置

1. 创建 `.env` 文件：
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

2. 在Python代码中加载：
```python
from dotenv import load_dotenv
load_dotenv()
```

## 获取OpenAI API密钥的步骤

1. **访问OpenAI官网**
   - 打开 https://platform.openai.com/
   - 点击右上角"Sign up"或"Log in"

2. **登录账户**
   - 使用邮箱或Google账户登录
   - 完成邮箱验证

3. **进入API密钥页面**
   - 登录后点击左侧菜单"API keys"
   - 或直接访问 https://platform.openai.com/api-keys

4. **创建新的API密钥**
   - 点击"Create new secret key"
   - 输入密钥名称（可选）
   - 点击"Create secret key"

5. **复制API密钥**
   - 系统会显示新创建的API密钥
   - **重要：立即复制并保存，因为这是唯一一次显示**
   - 密钥格式类似：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## 验证设置是否成功

创建一个测试文件 `test_api_key.py`：
```python
import os
from openai import OpenAI

# 检查环境变量
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("✓ OpenAI API密钥已设置")
    print(f"密钥前10位: {api_key[:10]}...")
    
    # 测试API连接
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✓ API连接测试成功")
    except Exception as e:
        print(f"✗ API连接测试失败: {e}")
else:
    print("✗ OpenAI API密钥未设置")
    print("请按照上述方法设置API密钥")
```

## 安全注意事项

1. **不要将API密钥提交到代码仓库**
   - 将 `.env` 文件添加到 `.gitignore`
   - 不要在代码中硬编码API密钥

2. **定期轮换API密钥**
   - 定期检查API使用情况
   - 如发现异常使用，立即更换密钥

3. **设置使用限制**
   - 在OpenAI控制台设置使用限额
   - 监控API调用频率和费用

## 常见问题

### Q: 密钥格式不正确？
A: OpenAI API密钥通常以 `sk-` 开头，长度为51个字符

### Q: 设置后仍然报错？
A: 检查：
- 密钥是否正确复制
- 环境变量是否生效（重启终端）
- 网络连接是否正常

### Q: 如何查看当前设置的环境变量？
```bash
# Linux/Mac
echo $OPENAI_API_KEY

# Windows
echo %OPENAI_API_KEY%
```

## 下一步

设置完成后，您就可以运行RAGAS评估测试了：
```bash
cd /root/AI-exploration/ragas_evaluation_demo
python3 ragas_demo.py
``` 