using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HeroBehaviour : MonoBehaviour
{
    public GameManager manager;
    public GameObject projectile;
    private bool dead = false;
    private bool invokerCalled = false;
    private Animator anim;

    void Start()
    {
        anim = gameObject.GetComponent<Animator>();
    }

    void OnCollisionEnter(Collision c)
    {
        if(c.collider.gameObject.transform.tag == "Enemy")
        {
            dead = true;
            anim.Play("DEAD",0,0);
            manager.GameOver(c.collider.gameObject);
        }
    }

    public void InvokeFireBullet()
    {
        if(!invokerCalled)
        {
            InvokeRepeating("FireBullet", 1f, 0.5f);
            invokerCalled = true;
        }
    }

    void FireBullet()
    {
        if(dead)
            return;

        anim.Play("SHOOTING", 0,0);
        Vector3 position = transform.position + new Vector3(0,0.07f,0);
        GameObject bullet = Instantiate(projectile, position, transform.rotation) as GameObject;
    }
}
