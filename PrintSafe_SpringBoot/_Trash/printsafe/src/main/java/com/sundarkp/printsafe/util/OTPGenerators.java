package com.sundarkp.printsafe.util;

import java.util.Random;

public class OTPGenerators {
    public static char[] OTP(int len)
    {
        System.out.println("Generating OTP using random() : ");
        System.out.print("You OTP is : ");
        String numbers = "0123456789";
        Random rndm_method = new Random();
  
        char[] otp = new char[len];
        for (int i = 0; i < len; i++)
        {
            otp[i] = numbers.charAt(rndm_method.nextInt(numbers.length()));
        }
        return otp;
    }
}
