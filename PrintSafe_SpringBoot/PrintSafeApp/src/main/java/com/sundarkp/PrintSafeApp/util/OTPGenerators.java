package com.sundarkp.PrintSafeApp.util;

import java.util.Random;

public class OTPGenerators {
    public static char[] OTP(int len)
    {
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
