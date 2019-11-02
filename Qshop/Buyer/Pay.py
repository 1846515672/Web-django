from alipay import AliPay

def pay(order_id, money):
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkuB6ySNwizrWJxNRYUrzf85JfEJleULsV4Tgqj9AGe8VZklXAz1dkxuNi6zkb01UHwkFuxxQk/SHhucCTIbkzdWfDD3wJFQmHvqz9Vs6uc8jidoHRQ2sN57i8d6BUMDZ8Parrn8ix1VuHpIC5iTSnUdZBPP3PBUt7Dfi7Ur3Ow6IkhFYkmmgRlWSITjQq8K3Rpfd4TufY2hcHI8BStQcBUEWHpotHjHGoytLROIAIF8ahGoxug9rCqDPCo+5JLEO+p2qvfnZ8ADQYZgrFHAsXTsQPjUQrPQMMAvuGzGc21KR8bTsIV7qAek/1eij6U7OE3F7bYKwNZnj+CbDB9U0TwIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEogIBAAKCAQEAkuB6ySNwizrWJxNRYUrzf85JfEJleULsV4Tgqj9AGe8VZklXAz1dkxuNi6zkb01UHwkFuxxQk/SHhucCTIbkzdWfDD3wJFQmHvqz9Vs6uc8jidoHRQ2sN57i8d6BUMDZ8Parrn8ix1VuHpIC5iTSnUdZBPP3PBUt7Dfi7Ur3Ow6IkhFYkmmgRlWSITjQq8K3Rpfd4TufY2hcHI8BStQcBUEWHpotHjHGoytLROIAIF8ahGoxug9rCqDPCo+5JLEO+p2qvfnZ8ADQYZgrFHAsXTsQPjUQrPQMMAvuGzGc21KR8bTsIV7qAek/1eij6U7OE3F7bYKwNZnj+CbDB9U0TwIDAQABAoIBAFtUmwVXtDPfcir6KDCHmsJuU+OgpdixdKU3SzyR+BooQPZJxIGPNxCyoWGpMKLFQvnJcnbXNIPMGjoYi6Vqe/xCSZQjL6Bncwzwd9ap0+qWk1K08LBPwDcV5ajg4yiDwwHDYR4wkD/DL6ZyxLq3Sv/hzcj2q1YBFX09gy5q3zEo9VPomnZxGgRYiyN5PUNOacIjs7hM0KgoR6xXtq1NSYY8aO0pdEMXM+Pw7tV1qJHUTEwXw+1mQwXmNuNteVw5vbBbKVQMAZ5dWZIJdpQl0oEeNEh2opJHmP08sABatzfljOHjy16zOha2vy8kBNvjWo+0h/AcYwwwb1hjIUAtPgECgYEA293dicAZYoJubdBQ1/UI28zgDK6n4eQAElnxhVufvnNEArQRt88WUFuSMAMDMK7GJtGj/Hrcd+S5fBy1PiFCi+Lxkd60mLWM4C3Gf51f3FuM33hdF8DyDFqwPbI/IU4IHuL5FhGQE6eZvvLhm2c/fXodQj7zw4QnN4NBcOsfMf8CgYEAqwPR0gs67iB09xyDQWeNDFHujvx/yGwNoPllro9kqwqqDzwuy0Rhkw5gmilrCON+1L0Z7tttvugh11dcqWNmTvbzZhGxeAq3iC2RfXJDB0s/5YyVqqs3GTtw6gVf5BD60K+/RU+kEK/W9FYXfeefzuvajsmeYiLNQvc+AsnmXbECgYAqhqtG7YT7bMb3Loe0fYyNFv9u9Ik8Q+FPq13vsV0gdSL+ct3Kc5+ZQ1zvNGX1kJh7Aal6ODlUZ0UJIHRd5Aj/DZIz6KN9tf/djH0MSeA0uvBweNNouMUYZqIYDNXxFyqy7qvG/PalFpHCQTAp4rqBBpGKMqrrcjAzqIuLz65k+QKBgCiuYe1baotXATv/dmHKpkz1+I/fFO6ydZODgGLEDah6gvXY1TDZdXSsCOLjU2jr5THqQg8F99dgFRzK1WoeESpbqI7xSoxJ0Fr+rAtxcOx9RBfxF3FgBV1lPHkPCj6Qo3mdNRzh0x99FN9O04vJ28Q3auhoodqqeLWjZwb2zGwhAoGAMl74n7XKzvqBh+A6AUXCotZKDqRMEehEyJSWg2Pa9e1rn0GK67uwUILoClPyz/Y4eP1l9mIOTaSoA8BjM6EABVw/KBYUSZ9gxkOPqqXDB+QVM33qLR1Y0Da7OTRKMWl4LUZ0603zUTAdrMNCxaxs4g1Ue6zu5viVDgYGDOQcvQc=
    -----END RSA PRIVATE KEY-----'''

    alipay = AliPay(
        appid="2016101500695900",  # 支付宝app的id
        app_notify_url="",  # 回调视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="商贸商城",
        return_url=None, #完成之后返回
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 让用户进行支付的支付宝页面网址
    return "https://openapi.alipaydev.com/gateway.do?" + order_string

if __name__ == '__main__':
    print(pay("1301000021","1999.9"))