

from Get_Data_From_Cell import Get_Battery_Data_Row # gets the row of data and puts it into an array


def Find_Power_Dense_Battery(battery_1, battery_2):
    battery_1 = Get_Battery_Data_Row(battery_1)
    battery_2 = Get_Battery_Data_Row(battery_2)

    

    battery_1_Wh = battery_1[14] * battery_1[16]
    battery_2_Wh = battery_2[14] * battery_2[16]

    if battery_1_Wh < battery_2_Wh:
        
        battery_3 = battery_1
        battery_1 = battery_2
        battery_2 = battery_3
        
        battery_1_Wh = battery_1[14] * battery_1[16]
        battery_2_Wh = battery_2[14] * battery_2[16]

    return battery_1, battery_2, battery_1_Wh, battery_2_Wh

def Find_Power_Dense_Battery_Efficient(battery_1, battery_2):
    
    battery_1_Wh = battery_1[14] * battery_1[16]
    battery_2_Wh = battery_2[14] * battery_2[16]
    
    if battery_1_Wh < battery_2_Wh:
        
        battery_3 = battery_1
        battery_1 = battery_2
        battery_2 = battery_3
        
        battery_1_Wh = battery_1[14] * battery_1[16]
        battery_2_Wh = battery_2[14] * battery_2[16]

    return battery_1, battery_2, battery_1_Wh, battery_2_Wh