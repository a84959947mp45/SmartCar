package com.example.myapplication;

import android.os.Bundle;


import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Button;
import android.widget.EditText;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import java.net.Socket;
import java.net.URL;
import java.net.HttpURLConnection;
import android.os.AsyncTask;
import java.io.InputStream;
import java.io.*;
import java.net.*;
import android.os.Handler;
import java.util.*;
public class MainActivity extends AppCompatActivity
{
	ImageView image;
	
	Handler handler = new Handler();
	String msg="";
	TextView message;
    TextView warning;
	String address = "192.168.1.10";// 連線的ip
	int port = 8888;
	java.io.BufferedInputStream in;
    java.io.BufferedWriter bw;
	java.io.ObjectInputStream in_client;
    Socket client;//與Server連線之socket
	@Override
    protected void onCreate(Bundle savedInstanceState) 
	{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
		image = (ImageView)findViewById(R.id.imageView);
		message = (TextView)findViewById(R.id.textView);
		warning = (TextView)findViewById(R.id.textView);
		
		
		
		image.setImageResource(R.drawable.android_icon_256);//圖片設定
		final Button button = findViewById(R.id.button);//按鈕給予

		button.setOnClickListener(new View.OnClickListener() 
		{
             public void onClick(View v)
			 {
				 EditText edit = findViewById(R.id.editText);
				 address = edit.getText().toString().trim();//取得文字
				 handler.postDelayed(updateText, 70);
                 new Thread(ServerConnection).start();
             }
         });
		//new DownloadImageTask((ImageView) findViewById(R.id.imageView)).execute("http://java.sogeti.nl/JavaBlog/wp-content/uploads/2009/04/android_icon_256.png");
		//new DownloadImageTask((ImageView) findViewById(R.id.imageView)).execute("http://192.168.1.10:8000/output.jpg");
	}
	 private Runnable ServerConnection = new Runnable()
    {
        //設定Delay的時間
        //網路設定
        public void run() 
		{
			
            //InetSocketAddress isa = new InetSocketAddress(this.address, this.port);
            try 
			{
                client = new Socket(address, port);
                //client.connect(isa, 10000);
            } 
			catch (android.os.NetworkOnMainThreadException e) 
			{
                message.setText(e.toString());
            } 
			catch (java.io.IOException e) 
			{
                //time.setText("SSS !!!");
                message.setText(e.toString());
            }

            int count=0;
            try
            {
                String data = "";
                in = new java.io.BufferedInputStream(client.getInputStream());
                bw = new java.io.BufferedWriter( new java.io.OutputStreamWriter(client.getOutputStream()));
				int length;
                byte[] b = new byte[80000];

                while ((length = in.read(b)) > 0)// <=0的話就是結束了
                {
                    data = new String(b, 0, length);

                    if(length==1)
						msg=data;
                    //寫入
                    bw.write("ok");
                    //立即發送
                    bw.flush();
                }
                client.close();
			}
            catch (java.io.IOException e)
            {
                warning.setText("Socket連線有問題 !");
                //time.setText("IOException :" + e.toString());
            }
			 catch (Exception e) 
			 {
                System.err.println("Server - Error transfering bitmaps: "+ e.getMessage());
			 }
        }
    };
	//固定要執行的方法
    private Runnable updateText = new Runnable() 
	{
        public void run()
        {
			String ans= msg;
			switch(msg) 
			{ 
				case "R": 
					ans="右轉";
					break; 
				case "L": 
					ans="左轉";
					break; 
				case "F":
					ans="前進";
					break; 
				default:
					ans="未偵測到";
			} 
            message.setText(ans);
			//warning.setText(Integer.toString(length)+","+msg);
			
			Log.e("Error","123");
            new DownloadImageTask((ImageView) findViewById(R.id.imageView)).execute("http://"+address+":8000/output.jpg");
			handler.postDelayed(this, 70);
		}
    };
	private class DownloadImageTask extends AsyncTask<String, Void, Bitmap> 
	{
		ImageView bmImage;
		 Hashtable<String, Bitmap> images;
		public DownloadImageTask(ImageView bmImage) 
		{
			this.bmImage = bmImage;
			if(images == null)
			{
				images = new Hashtable<String, Bitmap>();
			}
		}
		protected Bitmap doInBackground(String... urls) 
		{
			Bitmap image = images.get(urls[0]);
			if(image!=null)
			{
				return image;
			}
			String urldisplay = urls[0];
			Log.e("Error", urldisplay);
			Bitmap mIcon11 = null;
			try 
			{
				//client = new Socket("192.168.1.10", 8888);
				InputStream in = new java.net.URL(urldisplay).openStream();
				//InputStream in = client.getInputStream();
				mIcon11 = BitmapFactory.decodeStream(in);
				//client.close();
			} 
			catch (Exception e) 
			{
				Log.e("Error", e.getMessage());
				e.printStackTrace();
				return null;
			}
			if(mIcon11!=null)
			{
				images.put(urldisplay, mIcon11);
			}
			return mIcon11;
		}
		protected void onPostExecute(Bitmap result) 
		{
			if (result!=null)
				bmImage.setImageBitmap(result);
		}
	}
}
