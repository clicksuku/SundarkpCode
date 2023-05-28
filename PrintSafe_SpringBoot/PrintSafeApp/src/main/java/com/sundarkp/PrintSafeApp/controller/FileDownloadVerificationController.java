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
public class FileDownloadVerificationController {
    @Autowired
    private LocalCacheService cache;

    @RequestMapping(value = "/download/{fileCode}" , method=RequestMethod.GET)
    public String downloadFile(@PathVariable("fileCode") String fileCode, HttpSession session, RedirectAttributes redirectAttributes) {
        String otp = null;

        if(cache.getCacheElement(fileCode) !=null)
            otp = cache.getCacheElement(fileCode);
        else
        {
            otp = new String (OTPGenerators.OTP(6));    
            cache.addCacheElement(fileCode, otp);
        }
    
        session.setAttribute("fileCode", fileCode);    
        session.setAttribute("otp", otp);    
        return "downloadverify";
    }
    

}
