package com.sundarkp.printsafe.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;


import org.springframework.core.io.InputStreamResource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.http.MediaType;

@Controller
public class FileDownloadController {
    @RequestMapping(value = "/download" , method=RequestMethod.GET)
    public ResponseEntity<InputStreamResource> downloadFile(@ModelAttribute("downloadfile") String file) throws IOException{
        ResponseEntity<InputStreamResource> ipstream = downloadRedirect(file);
        return ipstream;
    }   

    private ResponseEntity<InputStreamResource>  downloadRedirect(String file)  throws IOException
    {
        File files = new File(file);
        String extension =  Files.probeContentType(Paths.get(file));
        InputStreamResource resource = new InputStreamResource(new FileInputStream(files));
        return ResponseEntity
                .ok()
                .contentLength(files.length())
                .header("Content-Disposition", "inline; filename=\"" + files.getName() + "\"")
                .contentType(
                   MediaType.parseMediaType(extension))
                .body(resource);
    }
}
