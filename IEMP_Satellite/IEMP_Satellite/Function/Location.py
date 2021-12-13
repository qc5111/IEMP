import OrderSendToClient
OrderSendToClient.WinClient("10.0.1.214","0123456789abcdef")
OrderSendToClient.SendOneCMDOrder('dumpsys location|grep "Location\\[" > test.log')
