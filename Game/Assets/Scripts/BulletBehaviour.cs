﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BulletBehaviour : MonoBehaviour
{
    private GameObject hero;
    private float speed = 1f;
    
    void Start()
    {
        hero =  GameObject.Find("Hero"); 
    }

    void Update()
    {
        if (Vector3.Distance(hero.transform.position, transform.position) > 1)
            Destroy(gameObject);
        else
            transform.position += transform.forward * Time.deltaTime * speed;
    }

    void OnCollisionEnter(Collision c)
    {
        if(c.collider.gameObject.transform.tag == "Wall")
            Destroy(gameObject);
    }
}
