package com.sundarkp.PrintSafeApp.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import com.sundarkp.PrintSafeApp.util.LocalCacheService;
import com.sundarkp.PrintSafeApp.util.OTPGenerators;

import jakarta.servlet.http.HttpSession;

@Controller
public class FileGenerateOtpController {
    @Autowired
    private LocalCacheService cache;

    @RequestMapping(value = "/generateotp/{fileCode}" , method=RequestMethod.GET)
    public String generateOtp(@PathVariable("fileCode") String fileCode, HttpSession session, RedirectAttributes redirectAttributes) {
        String otp = new String (OTPGenerators.OTP(6));     

        if(cache.getCacheElement(fileCode) !=null)
            cache.updateCacheElement(fileCode, otp);
        else    
            cache.addCacheElement(fileCode, otp);

        redirectAttributes.addFlashAttribute("otp", otp);    
        return "generateotp";
    }
    

}
