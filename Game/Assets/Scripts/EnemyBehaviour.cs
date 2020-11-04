using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyBehaviour : MonoBehaviour
{
    private GameObject hero;
    private GameManager manager;
    private float speed = 0.3f;
    public int health;
    public bool isCollider = false;
    Transform heroT;
    void Start()
    {
        hero =  GameObject.Find("Hero");
        manager = GameObject.Find("Manager").GetComponent<GameManager>(); 
        transform.LookAt(hero.transform);
        transform.Rotate(-90f,0,0);
        heroT = hero.transform;
    }

    // Update is called once per frame
    void Update()
    {
        if(!isCollider)
            transform.position += -transform.up * Time.deltaTime * speed;
    }

    void OnCollisionEnter(Collision c)
    {
        if(c.collider.gameObject.transform.tag == "Bullet")
        {
            health--;
            if(health <= 0)
            {
                Destroy(gameObject);
                manager.EnemyDown();
            }
            Destroy(c.collider.gameObject);
        }
    }
}
