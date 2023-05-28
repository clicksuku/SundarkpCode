package com.sundarkp.PrintSafeApp.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.springframework.core.io.InputStreamResource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import jakarta.servlet.http.HttpSession;

import org.springframework.http.MediaType;


@Controller
public class FileDownloadController {
    private static String UPLOADED_FOLDER_LOCAL = "/Users/sundar/Documents/Professional/Code/Ideation/PrintSafe/filesuploaded/";
    private String fileName;

    @RequestMapping(value = "/downloadverified" , method=RequestMethod.POST)
    public ResponseEntity<InputStreamResource> downloadFile(@RequestParam("otpentered") String otpentered, HttpSession session,RedirectAttributes redirectAttributes) throws IOException
    {

        String fileCode = (String) session.getAttribute("fileCode");
        String otp =  (String) session.getAttribute("otp");

        ResponseEntity<InputStreamResource> ipstream = null;
        
        if(otpentered.equals(otp)) 
        {
            ipstream = downloadRedirect(fileCode);
        
        }
        
        return ipstream;
    }   

    private ResponseEntity<InputStreamResource>  downloadRedirect(String fileCode)  throws IOException
    {
        String fileName = getFilePath(fileCode);
        File file = new File(getFilePath(fileCode));
        String extension =  Files.probeContentType(Paths.get(fileName));
        InputStreamResource resource = new InputStreamResource(new FileInputStream(file));
        return ResponseEntity
                .ok()
                .contentLength(file.length())
                .header("Content-Disposition", "inline; filename=\"" + file.getName() + "\"")
                .contentType(
                   MediaType.parseMediaType(extension))
                .body(resource);
    }

    private String getFilePath(String fileCode) throws IOException {
        Path dirPath = Paths.get(UPLOADED_FOLDER_LOCAL);
     
        Files.list(dirPath).forEach(file -> {
            if (file.getFileName().toString().startsWith(fileCode)) {
                fileName = UPLOADED_FOLDER_LOCAL + file.getFileName().toString();
                return;
            }
        });

        return fileName;
    }

}
