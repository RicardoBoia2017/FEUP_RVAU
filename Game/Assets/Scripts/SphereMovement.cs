using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SphereMovement : MonoBehaviour
{
    public GameObject hero;

//    private Text text;

    void Start()
    {
        hero =  GameObject.Find("Hero");
    }

    // Update is called once per frame
    void Update()
    {
        if(hero != null)
        {
            hero.transform.LookAt(transform);
        }
    }

    /*void OnCollisionEnter(Collision c)
    {
        if(c.collider.transform.name.Equals("Hero"))
            hero = c.collider.gameObject;
    }*/
}
