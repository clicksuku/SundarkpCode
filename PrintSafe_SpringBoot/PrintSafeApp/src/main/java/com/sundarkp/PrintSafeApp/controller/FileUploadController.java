package com.sundarkp.PrintSafeApp.controller;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.apache.commons.lang3.RandomStringUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import com.sundarkp.PrintSafeApp.model.FileUploadResponse;

@Controller
public class FileUploadController {
    private static String UPLOADED_FOLDER_LOCAL = "/Users/sundar/Documents/Professional/Code/Ideation/PrintSafe/filesuploaded/";

    @RequestMapping("/")    
    public String index()  
    {    
        return"upload";    
    }

    @RequestMapping(value="/upload", method=RequestMethod.POST)
    public ResponseEntity<FileUploadResponse> singleFileUpload(@RequestParam("file") MultipartFile file, 
                                    RedirectAttributes redirectAttributes ) {

        if (file.isEmpty()) {
            return new ResponseEntity<>(null, HttpStatus.INTERNAL_SERVER_ERROR);
        }

        Path path=null;
        String fileCode = null; 

        try {

            byte[] bytes = file.getBytes();
            fileCode = RandomStringUtils.randomAlphanumeric(8);
            
            path = Paths.get(UPLOADED_FOLDER_LOCAL + fileCode + "_" + file.getOriginalFilename());
            Files.write(path, bytes);

        } catch (IOException e) {
            e.printStackTrace();
        } 

        FileUploadResponse fup = new FileUploadResponse();
        fup.setDownloadUri("/generateotp/"+ fileCode);
        fup.setFileName(file.getOriginalFilename());
        return new ResponseEntity<>(fup,HttpStatus.OK);
    }

    @GetMapping("/uploadstatus")
    public String uploadStatus() {
        return "uploadstatus";
    }
}
