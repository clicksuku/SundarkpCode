package com.sundarkp.printsafe.controller;

import java.io.DataOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.net.URL;
import java.net.URLConnection;
import java.net.HttpURLConnection;
import java.net.Proxy;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
public class FileUploadController {
    //Save the uploaded file to this folder
    private static String UPLOADED_FOLDER_LOCAL = "/Users/sundar/Documents/Professional/Code/Ideation/PrintSafe/filesuploaded/";
    private static String UPLOADED_FOLDER_HTTP = "http://localhost:8000/";

    @RequestMapping("/")    
    public String index()  
    {    
        return"upload";    
    }

    /*@RequestMapping(value="/upload", method=RequestMethod.POST)
    public ResponseEntity<?> simple(@RequestParam("uri") String uri) {
        return ResponseEntity.status(201).body("Created!"); 
    }*/
    
    
    /*@RequestMapping(value="/upload", method=RequestMethod.POST)
    public ResponseEntity<?> singleFileUpload(@RequestParam("file") MultipartFile file 
                                   RedirectAttributes redirectAttributes ) {*/

    @RequestMapping(value="/upload", method=RequestMethod.POST)
    public String singleFileUpload(@RequestParam("file") MultipartFile file, 
                                    RedirectAttributes redirectAttributes ) {

        if (file.isEmpty()) {
            //redirectAttributes.addFlashAttribute("message", "Please select a file to upload");
            //return "redirect:/uploadstatus";
            //return ResponseEntity.status(501).body("File Upload failed!"); 
            redirectAttributes.addFlashAttribute("downloadfile", "null");
            return "redirect:/download";
        }

        try {

            // Get the file and save it somewhere
            byte[] bytes = file.getBytes();
            Path path = Paths.get(UPLOADED_FOLDER_LOCAL + file.getOriginalFilename());
            Files.write(path, bytes);
            System.out.println(path);

            //redirectAttributes.addFlashAttribute("message","You successfully uploaded '" + file.getOriginalFilename() + "'");

        } catch (IOException e) {
            e.printStackTrace();
        } 

        //return "redirect:/uploadstatus";
        //return ResponseEntity.status(201).body("File Uploaded!"); 
        redirectAttributes.addFlashAttribute("downloadfile", UPLOADED_FOLDER_LOCAL + file.getOriginalFilename() );
        return "redirect:/download";
    }

    @GetMapping("/uploadstatus")
    public String uploadStatus() {
        return "uploadstatus";
    }

    @RequestMapping(value="/uploadhttp", method=RequestMethod.POST)
    public String singleFileUploadToHTTP(@RequestParam("file") MultipartFile file,
                                   RedirectAttributes redirectAttributes) {

        if (file.isEmpty()) {
            redirectAttributes.addFlashAttribute("message", "Please select a file to upload");
            return "redirect:/uploadstatus";
        }

        URL url;
        URLConnection urlconnection=null;
        DataOutputStream dos;

        try {

            //URI uri = new URI("http://","localhost:2343","");
            url = new URL(UPLOADED_FOLDER_HTTP);
            urlconnection = url.openConnection(Proxy.NO_PROXY);

			urlconnection.setDoOutput(true);
			urlconnection.setDoInput(true);
            urlconnection.setUseCaches(false);

            if (urlconnection instanceof HttpURLConnection) {
				((HttpURLConnection) urlconnection).setRequestMethod("POST");
				((HttpURLConnection) urlconnection).setRequestProperty("Content-type", "multipart/form-data");
				((HttpURLConnection) urlconnection).connect();
			}

			dos = new DataOutputStream(urlconnection.getOutputStream());
			byte[] bytes = file.getBytes();
            dos.write(bytes);
            dos.flush();
            dos.close();

            ((HttpURLConnection) urlconnection).disconnect();

            redirectAttributes.addFlashAttribute("message",
                    "You successfully uploaded '" + file.getOriginalFilename() + "'");

        } catch (IOException e) {
            e.printStackTrace();
        } 
    
        //return new RedirectView("/uploadstatus");
        return "redirect:/uploadstatus";
    }
}
