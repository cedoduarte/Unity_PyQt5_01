// este script va referenciado a un Cubo

using System;
using System.Text;
using System.Collections;
using System.Collections.Generic;

using UnityEngine;

using System.Net;
using System.Net.Sockets;
using System.Threading;

public class start : MonoBehaviour
{
    private Vector3 pos;    
    private Quaternion rot;
    private float wrot;
    private Vector3 scale;
    private TcpClient socket;
    private Thread thread;

    private TcpClient MakeSocket(string host, int port)
    {
        TcpClient sock = new TcpClient(host, port);
        return sock;
    }

    private Thread MakeThread()
    {
        try
        {
            Thread th = new Thread(new ThreadStart(this.OnSocketReadyRead));
            th.IsBackground = true;
            return th;
        }
        catch (Exception ex)
        {
            Debug.Log(ex);
        }
        return null;
    }

    private void OnSocketReadyRead()
    {
        try
        {
            // declaración de variables
            string message;
            string data;
            string aux;
            string txt;

            int length;

            float xpos, ypos, zpos;
            float xrot, yrot, zrot;
            float xscale, yscale, zscale;

            byte[] incomingData;
            Byte[] bytes = new Byte[1024];

            NetworkStream stream;

            while (true)
            {
                stream = socket.GetStream();
                do
                {
                    length = stream.Read(bytes, 0, bytes.Length);
                    incomingData = new byte[length];
                    Array.Copy(bytes, 0, incomingData, 0, length);
                    message = Encoding.ASCII.GetString(incomingData);
                    Debug.Log("From server: " + message);

                    if (message.Contains("_to_unity_parameters_"))
                    {
                        data = message.Replace("_to_unity_parameters_(", "");
                        data = data.Replace(")", "");

                        aux = "xpos=";
                        txt = data.Substring(data.IndexOf(aux)+aux.Length);
                        txt = txt.Substring(0, txt.IndexOf(";"));
                        xpos = float.Parse(txt);

                        aux = "ypos=";
                        txt = data.Substring(data.IndexOf(aux) + aux.Length);
                        txt = txt.Substring(0, txt.IndexOf(";"));
                        ypos = float.Parse(txt);

                        aux = "zpos=";
                        txt = data.Substring(data.IndexOf(aux) + aux.Length);
                        txt = txt.Substring(0, txt.IndexOf(";"));
                        zpos = float.Parse(txt);

                        aux = "xrot=";
                        txt = data.Substring(data.IndexOf(aux) + aux.Length);
                        txt = txt.Substring(0, txt.IndexOf(";"));
                        xrot = float.Parse(txt);

                        aux = "yrot=";
                        txt = data.Substring(data.IndexOf(aux) + aux.Length);
                        txt = txt.Substring(0, txt.IndexOf(";"));
                        yrot = float.Parse(txt);

                        aux = "zrot=";
                        txt = data.Substring(data.IndexOf(aux) + aux.Length);
                        txt = txt.Substring(0, txt.IndexOf(";"));
                        zrot = float.Parse(txt);

                        aux = "xscale=";
                        txt = data.Substring(data.IndexOf(aux) + aux.Length);
                        txt = txt.Substring(0, txt.IndexOf(";"));
                        xscale = float.Parse(txt);

                        aux = "yscale=";
                        txt = data.Substring(data.IndexOf(aux) + aux.Length);
                        txt = txt.Substring(0, txt.IndexOf(";"));
                        yscale = float.Parse(txt);

                        aux = "zscale=";
                        txt = data.Substring(data.IndexOf(aux) + aux.Length);
                        txt = txt.Substring(0);
                        zscale = float.Parse(txt);

                        this.pos = new Vector3(xpos, ypos, zpos);
                        this.rot = new Quaternion(xrot, yrot, zrot, this.wrot);
                        this.scale = new Vector3(xscale, yscale, zscale);                        
                    }
                    else if (message.Contains("_to_unity_abort_"))
                    {
                        return;
                    }
                }
                while (length != 0);
            }
        }
        catch (Exception ex)
        {
            Debug.Log(ex);
        }
    }

    private void SendData(string msg)
    {
        try
        {
            byte[] data;
            NetworkStream stream;

            if (socket != null)
            {
                stream = socket.GetStream();
                if (stream.CanWrite)
                {
                    data = Encoding.ASCII.GetBytes(msg);
                    stream.Write(data, 0, data.Length);
                    Debug.Log("Message sent: " + msg);
                }
            }
        }
        catch (Exception ex)
        {
            Debug.Log(ex);
        }
    }

    private void initCubeProperties()
    {
        // iniciamos valores del cubo
        this.pos = transform.position;
        this.wrot = transform.rotation.w;
        this.rot = transform.rotation;        
        this.scale = transform.localScale;
    }

    private void initThread()
    { 
        // iniciamos thread
        this.socket = MakeSocket("localhost", 12345);
        this.thread = MakeThread();
        this.thread.Start();
        SendData("Unity ready...");
    }

    private void sendCubeProperties()
    {
        // enviamos información al servidor de PyQt5
        string data = "_to_pyqt_parameters_(xpos={0};ypos={1};zpos={2};xrot={3};yrot={4};zrot={5};xscale={6};yscale={7};zscale={8})";
        data = string.Format(data, this.pos.x, this.pos.y, this.pos.z, this.rot.x, this.rot.y, this.rot.z, this.scale.x, this.scale.y, this.scale.z);
        SendData(data);
    }

    void Start()
    {
        initCubeProperties();
        initThread();
        sendCubeProperties();
    }

    void Update()
    {
        // actualizamos propiedades del cubo
        transform.position = this.pos;
        transform.rotation = this.rot;
        transform.localScale = this.scale;
    }
}