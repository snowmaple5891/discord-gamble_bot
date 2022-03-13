# discord_gamblebot
A discord bot with simple commands to gamble or play games with unreal currency on discord

---

# BOT introduction
## functions and commands

#### blackjack.py

    ;create_bjgame
    create blackjack game text
![image](https://user-images.githubusercontent.com/80057212/158068855-d0b1154c-c3d3-4cc7-9872-3992b2b87b6f.png)

    ;joingame [amount]
    join blackjack game and update the previous message by editting it
![image](https://user-images.githubusercontent.com/80057212/158068900-d843836f-f3af-4c11-99b3-1702f138f7e0.png)

    ;startgame
    the discord bot will DM you which card you draw
|the channel you start Blackjack game|DM channel|
|:----:|:----:|
|![image](https://user-images.githubusercontent.com/80057212/158069106-c7a2ac3b-2cc1-413e-80d0-35263b472203.png)|![image](https://user-images.githubusercontent.com/80057212/158069113-b949f49a-91ba-49f3-b459-632aa85a7df7.png)|

    ;hit
    draw another card
![image](https://user-images.githubusercontent.com/80057212/158069154-ccb8d0b3-f3c0-4cb5-bbf4-a0a625e0eb60.png)

    ;stand
    end doing operation to your cards, you will get a hyperlink to tranfer back to the previous channel
![image](https://user-images.githubusercontent.com/80057212/158071115-af4146b1-8930-42df-9b6b-8a7000b96b67.png)

#### RESULT
 - the time in the footage is UTC+8

![image](https://user-images.githubusercontent.com/80057212/158069268-47719698-ee36-46d6-8903-b8dead17df0a.png)

#### gamble_entertain.py

    ;timely
    withdraw your money every 9 hours
![image](https://user-images.githubusercontent.com/80057212/158070892-f5529c56-452a-4ac2-a3f7-386ea170166d.png)

    ;br [amount]
    Bets a certain amount of money by rolling a dice
    if you rolled 1, yields x5 of your currency
    rolling over 66 yields x2 of your currency, over 90 -> x4 and over 100 -> x10
    For Examble: ;br 100
![image](https://user-images.githubusercontent.com/80057212/158070912-dce2ad3d-1cd0-4720-9583-3ca74b0628ff.png)

    ;bf [amount] [orientation]
    flip a coin and guess which direction it is facing, h = head, t = tail
    For Examble: ;bf 100 h
![image](https://user-images.githubusercontent.com/80057212/158070924-571f48c6-b22c-41d1-a361-dd7eb845bf82.png)

    ;wheel [amount]
    bet your currency by turning a wheel
    For Examble: ;wheel 100
![image](https://user-images.githubusercontent.com/80057212/158067018-65e8e580-8ff2-4b8d-ac00-373bea90c0b2.png)

#### gamble_function.py

    ;info
    show your total money

    ;donate [target] [amount]
    For Example: ;donate @雪楓OuO 200
    
    ;lb
    show total currency leader board in this guild
    
    ;shop
    show shop detail, merchandise and price
    
    ;buy [index]
    buy certain merch in shop
    (this function only include money decrement)
    
    ;add_merch(for guild manager only)
    add merchandise to shop

## remain archives
#### gamble_config.py
 - several functions to support situation judgment

#### gamble_manage.py
 - commands for guild manager to better manage their guild

#### gamble_event.py
 - a function for guild members to can get specific roles by adding reaction to specific message

---

# bot settings and other related
## setting.json
#### remember to put your ***DISCORD BOT TOKEN*** in this file, look at the following picture for more details
    transmit information in setting.json: use jdata[key] and insert the following coding on top of your code
![image](https://user-images.githubusercontent.com/80057212/158069982-e2031a2a-bab6-4919-a85d-41128cf1d499.png)
![image](https://user-images.githubusercontent.com/80057212/158070105-a5b62756-97b7-4611-84d9-1f32b0f94e4b.png)

## extension.txt
#### type your remain files name in this txt file because the main file must know which file to load while excecuting the bot 
![image](https://user-images.githubusercontent.com/80057212/158070417-834a3e3e-53b0-492a-a49d-3102931b93cc.png)

![image](https://user-images.githubusercontent.com/80057212/158070524-1f431835-0518-406c-9ced-c0117f1ffc46.png)

---

# Endings
### this code is free for any usage
### feel free to ask me any question about this code on discord

## Author
#### Girhub: snowmaple5891
#### Gmail: shenyue0602@gmail.com
#### Discord:
 - name: 雪楓OuO
 - discriminator(#): 2021
