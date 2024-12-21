package com.sundarkp.PrintSafeApp.util;

import java.util.concurrent.ConcurrentHashMap;
import org.springframework.context.annotation.Configuration;

@Configuration
public class LocalCacheService {
    private ConcurrentHashMap<String, String> filesMap = new ConcurrentHashMap<>();

    public void addCacheElement(String fileCode, String otp)
    {
        filesMap.put(fileCode,otp);
    }

    public void updateCacheElement(String fileCode, String otp)
    {
        filesMap.replace(fileCode,otp);
    }


    public String getCacheElement(String fileCode)
    {
        return filesMap.get(fileCode);
    }

    public void removeCacheElement(String fileCode)
    {
        filesMap.remove(fileCode);
    }

    
}
