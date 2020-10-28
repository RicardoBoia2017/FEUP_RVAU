﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyBehaviour : MonoBehaviour
{
    private GameObject hero;
    private float speed = 0.5f;
    // Start is called before the first frame update
    void Start()
    {
        hero =  GameObject.Find("Hero");
    }

    // Update is called once per frame
    void Update()
    {
        transform.position = Vector3.MoveTowards(transform.position, hero.transform.position, speed * Time.deltaTime);
    }

    void OnCollisionEnter(Collision c)
    {
        if(c.collider.gameObject.transform.tag == "Bullet")
        {
            Debug.Log("DESTROYED");
            Destroy(gameObject);
            Destroy(c.collider.gameObject);
        }
    }
}
