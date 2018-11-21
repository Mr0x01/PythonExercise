import joycity_function


if __name__ == "__main__":
    username = "your mobile number"
    password = "your password"
    result = joycity_function.login(username,password)
    if result.result == "OK" :
        joycity_function.check_in(result.msg)
        input("运行完毕，即将退出。")